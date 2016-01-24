import requests


def get_citation_styles():
    r = requests.get('http://pkp-udev.lib.sfu.ca/api/job/citationStyleList')
    response = r.json()

    # response data
    flash_messages = response['flashMessages']
    status = response['status']
    citation_styles = response['citationStyles']
    if status == 'success':
        return citation_styles
