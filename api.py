import requests

from settings import SERVICE_URL


class Job():
    """
    PKP XML Parsing Service API for conversion job.
    """

    def submit(user_email, user_password, input, content, citation_style_hash):
        """Example request:
        http://example.com/api/job/submit
        POST parameters:
            'email' : 'user@example.com'
            'password' : 'passowrd'
            'fileName' : 'document.docx'
            'citationStyleHash' : 'c6de5efe3filenamefilename294b26391ea343053c19a84',
            'fileContent' : '...'

        Example response:
        {"status":"success","id":123}
        """
        # parameters
        URL = SERVICE_URL + 'api/job/submit'
        params = {
            'email':user_email,
            'password':user_password,
            'fileName':input,
            'fileContent':content,
            'citationStyleHash':citation_style_hash,
        }

        # request
        response = requests.post(URL, params)

        # response content
        content = response.json()
        status = content['status']
        id = content['id']
        flash_messages = content['flashMessages']

        # response usage
        if status == 'success':
            return id

    def status(user_email, user_password, job_id):
        """Example request:
        http://example.com/api/job/status?email=user@example.com&password=password&id=123

        Example response:
        {"status":"success","jobStatus":0,"jobStatusDescription":"Pending"}
        """
        # parameters
        URL = SERVICE_URL + 'api/job/status'
        params = {
            'email':user_email,
            'password':user_password,
            'id':job_id,
        }

        # request
        response = requests.get(URL, params)

        # response content
        content = response.json()
        status = content['status']
        job_status = content.get('jobStatus', 0)
        job_status_description = content.get('jobStatusDescription', '')
        error = content.get('error', '')
        flash_messages = content['flashMessages']

        # response usage
        if status == 'success':
            # if job_status is 2 # Completed
            return job_status

    def retrieve(user_email, user_password, job_id, conversion_stage, binary=False):
        """Example request:
        http://example.com/api/job/retrieve?email=user@example.com&password=password&id=123&conversionStage=10

        Example response:
        The requested document or a JSON string with an error message.
        """
        # parameters
        URL = SERVICE_URL + 'api/job/retrieve'
        params = {
            'email':user_email,
            'password':user_password,
            'id':job_id,
            'conversionStage':conversion_stage,
        }

        # request
        response = requests.get(URL, params)

        # response content
        if binary:
            content = response.content
        else:
            content = response.text

        # response usage
        return content  # output : converted file content (binary or text)

    def citation_style_list():
        """Example request:
        http://example.com/api/job/citationStyleList

        Example response:
        {"status":"success","citationStyles":{"c6de5efe3294b26391ea343053c19a84":"ACM SIG Proceedings (\u0022et al.\u0022 for 15+ authors)"...
        """
        # parameters
        URL = SERVICE_URL + 'api/job/citationStyleList'

        # request
        response = requests.get(URL)

        # response content
        content = response.json()
        status = content['status']
        flash_messages = content['flashMessages']
        citation_styles = content['citationStyles']

        # response usage
        if status == 'success':
            return citation_styles
