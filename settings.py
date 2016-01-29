# XMLPS
SERVICE_URL = 'http://pkp-udev.lib.sfu.ca/'

SUPPORTED_INPUT_FORMATS = (
    'pdf',
    'doc',
    'docx',
    'odt',
)

SUPPORTED_OUTPUT_FORMATS = {
    'zip':{
        # all files
        'conversion_stage':10,
        'binary':True,
        'ext':'zip',
    },
    'xml':{
        # JATS (NLM3) XML
        'conversion_stage':14,
        'binary':False,
        'ext':'nlm3.xml',
    },
    'epub':{
        # EPUB
        'conversion_stage':11,
        'binary':True,
        'ext':'epub',
    },
    'ref':{
        # references
        'conversion_stage':3,
        'binary':False,
        'ext':'bib.xml',
    },
    'bib':{
        # bibtex
        'conversion_stage':4,
        'binary':False,
        'ext':'bib',
    },
    'ner':{
        # named entities relations in JSON
        'conversion_stage':17,
        'binary':False,
        'ext':'ner.json',
    },
    'xmp':{
        # XMP extensible metadata platform
        'conversion_stage':9,
        'binary':False,
        'ext':'xmp.pdf',
    },
    'html':{
        # HTML in zip file with and assets
        'conversion_stage':6,
        'binary':True,
        'ext':'html.zip',
    },
    'docx':{
        # WP_IN = ?
        'conversion_stage':15,
        'binary':True,
        'ext':'docx',
    },
    # supported ?
    # 'pdf':{
    #     # PDF
    #     'conversion_stage':8,
    #     'binary':True,
    #     'ext':'pdf',
    # },
    # 'pdf_in':{
    #     # PDF as input?
    #     'conversion_stage':16,
    #     'binary':True,
    #     'ext':'in.pdf',
    # },
    # 'cit':{
    #     # citation style
    #     'conversion_stage':7,
    #     'binary':True,
    #     'ext':'docx',
    # },
}

CITATION_STYLE_HASH = '3f0f7fede090f24cc71b7281073996be'    # 'American Psychological Association 6th edition'
OUTPUT_FORMAT = 'xml'

WAIT_FOR_RETRIEVE = 60   # seconds

# login
USER_EMAIL = 'set real value in conf.py'
USER_PASSWORD = 'set real value in conf.py'

# data persistence
FILES_PICKLE = 'files.p'

from conf import * # noqa
