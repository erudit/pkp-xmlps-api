import argparse
from datetime import datetime as dt
import os
import pickle
import requests
import sys
import time

import api
from settings import (
    SUPPORTED_INPUT_FORMATS,
    SUPPORTED_OUTPUT_FORMATS,
    CITATION_STYLE_HASH,
    OUTPUT_FORMAT,
    WAIT_FOR_RETRIEVE,
    USER_EMAIL,
    USER_PASSWORD,
    FILES_PICKLE,
)


class ParsedFile(object):
    """File submitted to the service and its parsing information.
    """

    def __init__(self, filepath):
        # identification
        self.filepath = filepath
        self.dirname = os.path.dirname(filepath)
        self.filename = os.path.basename(filepath)
        split = self.filename.split('.')
        self.ext = split[-1]
        self.name = '.'.join(split[:-1])
        # submit
        self.input_filename = self.filename
        self.input_path = self.filepath
        self.citation_style_hash = CITATION_STYLE_HASH
        self.dt_submitted = None
        # job
        self.job_id = None
        self.job_status = None
        # retrieve
        self.output_format = None
        self.output_binary = None
        self.output_filename = None
        self.output_path = None
        self.dt_retrieved = None

    def to_submit(self):
        # to submit if we don't have a job id for this file yet
        if not self.job_id:
            return True
        else:
            return False

    def submit(self):
        if self.to_submit():

            # pre-call
            with open(self.input_path, 'rb') as f:
                content = f.read()

            params = {
                'user_email':USER_EMAIL,
                'user_password':USER_PASSWORD,
                'input_filename':self.input_filename,
                'content':content,
                'citation_style_hash':self.citation_style_hash,
            }

            # API submit call
            id = api.Job.submit(**params)

            # post-call
            if id:
                self.job_id = id
                self.dt_submitted = dt.now()
                self.report_submission()

    def status_ok(self):
        # if job_status is 2 : it means job is completed
        if self.job_status is 2:
            return True
        else:
            return False

    def status(self):
        if self.job_id and not self.status_ok():

            # pre-call
            params = {
                'user_email': USER_EMAIL,
                'user_password': USER_PASSWORD,
                'job_id': self.job_id,
            }

            # API status call
            job_status = api.Job.status(**params)

            # post-call
            self.job_status = job_status

    def to_retrieve(self):
        # to be retrieved if we know that status is ok
        if self.status_ok() and not self.dt_retrieved:
            return True
        else:
            return False

    def retrieve(self):
        if not self.to_retrieve():
            # update the status once
            self.status()

        if self.to_retrieve():

            # pre-call
            self.output_format = OUTPUT_FORMAT
            fileformat = SUPPORTED_OUTPUT_FORMATS[self.output_format]
            conversion_stage = fileformat['conversion_stage']
            params = {
                'user_email': USER_EMAIL,
                'user_password': USER_PASSWORD,
                'job_id': self.job_id,
                'conversion_stage': conversion_stage,
            }

            # API retrieve call
            response = api.Job.retrieve(**params)

            # post-call
            if response:
                ext = fileformat['ext']
                self.output_binary = fileformat['binary']
                self.output_filename = self.name + '.' + ext
                self.output_path = self.dirname + '/' + self.output_filename

                if self.output_binary:
                    mode = 'wb'
                    with open(self.output_path, mode) as f:
                        f.write(response.content)
                else:
                    mode = 'w'
                    with open(self.output_path, mode) as f:
                        f.write(response.text)

                self.dt_retrieved = dt.now()
                self.report_retrieval()

    def report_submission(self):
        print("{} : {}".format(
                self.input_filename,
                self.job_id or 'failed',
            )
        )

    def report_retrieval(self):
        print("{} : {}".format(
                self.filename,
                self.output_filename or 'failed',
            )
        )

    def __str__(self):
        if self.to_submit():
            todo = 'to submit'
        elif self.to_retrieve():
            todo = 'to retrieve'
        else:
            todo = 'done'
        return "{:>5} : {:s} --> {:s} [{:s}]".format(
            self.job_id or '<id?>',
            self.input_filename or '<input?>',
            self.output_filename or '<output?>',
            todo,
        )


def  get_files(path):
    """Returns a dict where full input file path is the key and a
    ParsedFile object is the value.
    """
    # load files already processed
    if os.path.isfile(FILES_PICKLE):
        files = pickle.load(open(FILES_PICKLE, 'rb'))
    else:
        files = {}

    # add requested files
    if os.path.isfile(path) and path not in files:
        f = ParsedFile(path)
        if f.ext in SUPPORTED_INPUT_FORMATS:
            files[path] = f
    else:
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                filepath = dirpath + '/' + filename
                if filepath not in files:
                    f = ParsedFile(filepath)
                    if f.ext in SUPPORTED_INPUT_FORMATS:
                        files[filepath] = f
    return files


def save_files(files):
    pickle.dump(files, open(FILES_PICKLE, 'wb'))

def cli_parse_args():

    # parsers
    parser = argparse.ArgumentParser(
        description='Calls PKP XML Parsing Service API.',
    )
    subparsers = parser.add_subparsers(
        help='sub-command help',
        dest='command',
    )

    # path argument
    path_arg = {
        'dest':'path',
        'type':str,
        'nargs':'?',  # path is not required
        'default':'data',
        'help':"""Path of the local file to submit to the service.
        ex.: python api.py submit data/1017687ar/Input.doc
        Or path of a directory to submit : all .pdf, .doc, .docx or .odt files
        will be automatically submitted.
        ex.: python api.py submit path/to/my/data
        Default path : data
        """,
    }

    # commands
    submit = subparsers.add_parser(
        'submit',
        help='Submits the given local file(s) to the service.',
    )
    submit.add_argument(**path_arg)

    retrieve = subparsers.add_parser(
        'retrieve',
        help='Retrieves the JATS output file from the service for the given id.',
    )
    retrieve.add_argument(**path_arg)

    parse = subparsers.add_parser(
        'parse',
        help='Submits file(s) to and retrieves output(s) from the service.',
    )
    parse.add_argument(**path_arg)
    parse.add_argument(
        '--wait',
        '-w',
        type=int,
        required=False,
        default=WAIT_FOR_RETRIEVE,
        help="""Time in seconds waited between submission call and retrieve call
        (giving time to the service to process). Defaults to {:d} seconds.
        """.format(WAIT_FOR_RETRIEVE)
    )

    return parser.parse_args()

if __name__ == '__main__':
    args = cli_parse_args()
    files = get_files(args.path)

    if not files:
        print('No compatible files with : {:s}'.format(
                args.path,
            )
        )
    else:
        # report
        WIDTH = 40

        # report header
        print(' ' * WIDTH)
        print('PKP XML Parsing Service')
        print('=' * WIDTH)

        # report body
        if args.command == 'submit':
            print('SUBMITTING')
            print('-' * WIDTH)
            for filepath, f in files.items():
                f.submit()
        elif args.command == 'retrieve':
            print('RETRIEVING')
            print('-' * WIDTH)
            for filepath, f in files.items():
                f.retrieve()
        elif args.command == 'parse':
            print('SUBMITTING')
            print('-' * WIDTH)
            for filepath, f in files.items():
                f.submit()
            print(' ' * WIDTH)
            time.sleep(args.wait)
            print('RETRIEVING')
            print('-' * WIDTH)
            for filepath, f in files.items():
                f.retrieve()

        # report footer
        print(' ' * WIDTH)
        print('FINAL REPORT')
        print('-' * WIDTH)
        for filename, f in files.items():
            print(f)
        print(' ' * WIDTH)
        save_files(files)
