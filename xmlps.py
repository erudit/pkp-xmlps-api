import argparse
from datetime import datetime as dt
import os
import requests
import sys
import time

from settings import (
    USER_EMAIL,
    PASSWORD,
    SUPPORTED_INPUT_FORMATS,
    WAIT_FOR_RETRIEVE,
)


class ParsedFile(object):
    """File submitted to the service and its parsing information.
    """

    def __init__(self, filepath):
        # identification
        self.filepath = filepath
        self.dirname = os.path.dirname(filepath)
        self.filename = os.path.basename(filepath)
        self.name, self.ext = self.filename.split('.')
        self.xmlps_id = None
        # submit
        self.input = self.filename
        self.input_path = self.filepath
        self.dt_submitted = None
        # retrieve
        self.output = None
        self.output_path = None
        self.dt_retrieved = None

    def submit(self):
        # pre-processing
        content = ''
        with open(self.input_path, 'rb') as f:
            content = f.read()

        post = {
            'email':USER_EMAIL,
            'password':PASSWORD,
            'fileName':self.input,
            'citationStyleHash':'3f0f7fede090f24cc71b7281073996be',
            'fileContent':content,
        }

        # API submit call

        # post-processing
        self.dt_submitted = dt.now()

    def retrieve(self):
        # API retrieve call

        # post-processing
        self.output = self.name + '.jats.xml'
        self.output_path = self.dirname + '/' + self.output
        self.dt_retrieved = dt.now()

    def __str__(self):
        return "{:>5} : {:s} --> {:s}".format(
            self.xmlps_id or '<id?>',
            self.input or '',
            self.output or '<to-retreive>',
        )


def  get_files(path):
    """Returns a dict where full input file path is the key and a
    ParsedFile object is the value.
    """
    files = {}
    if os.path.isfile(path):
        f = ParsedFile(path)
        if f.ext in SUPPORTED_INPUT_FORMATS:
            files[path] = f
    else:
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                filepath = dirpath + '/' + filename
                f = ParsedFile(filepath)
                if f.ext in SUPPORTED_INPUT_FORMATS:
                    files[filepath] = f
    return files


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
            print('SUBMITTED')
            print('-' * WIDTH)
            for filepath, f in files.items():
                # f.submit()
                print(f)
        elif args.command == 'retrieve':
            print('RETRIEVED')
            print('-' * WIDTH)
            for filepath, f in files.items():
                #f.retrieve()
                print(f)
        elif args.command == 'parse':
            print('SUBMITTED')
            print('-' * WIDTH)
            for filepath, f in files.items():
                #f.submit()
                print(f)
            print(' ' * WIDTH)
            time.sleep(args.wait)
            print('RETRIEVED')
            print('-' * WIDTH)
            for filepath, f in files.items():
                #f.retrieve()
                print(f)

        # report footer
        print(' ' * WIDTH)
