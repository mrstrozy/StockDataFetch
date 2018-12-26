
from message import Message

import requests
import json

class Connection(object):

    def __init__(self, host, output=None):
        self.host = host
        self.output = output if output else Message()
        self.session = None
        self.response = None
        self.data = None


    def establish_connection(self):
        '''
        This is used to establish a requests.Session with the host in
        this class.
        '''

        if self.session:
            msg = "[Note] In Connection.establish_connection -> "\
                  "Session already exists."
            return True

        self.session = requests.Session()


        if not self.session:
            msg = "Connection.make_connection() -> Unable to create session."
            self.output.error(msg)
            return False

        return True

    def terminate_connection(self):
        '''
        Used to terminate active session.
        '''
        if self.session:
            self.session.close()
            return True

        msg = "[Note] In Connection.terminate_connection -> "\
              "No active session exists."
        self.output.notify(msg)
        return True

    def make_request(self, 
                    fargs=None, 
                    resource='/graze/v1/', 
                    function='',
                    request_type='GET', 
                    headers=None, 
                    auth=None,
                    expectResponse=True):
        '''
        Used to make a web request for accessing information. Right now it
        is defaulted for the moog graze API.
        '''

        request_type = request_type.lower()
        if request_type not in ('get', 'post'):
            msg = "[Error]: In Connection.make_request -> "\
                  "Invalid Request Type: "+request_type+". "\
                  "Request Type must be either GET or POST."
            self.output.error(msg)
            return ({}, False)

        if not headers:
            headers = {'Content-Type': 'application/json; charset=UTF-8'}

        url_path = self.host + resource + function

        #print("Url path is: "+url_path)



        try:
            if request_type in 'get':
                self.response = self.session.get(url_path,
                                                params=fargs,
                                                headers=headers,
                                                auth=auth)
            elif request_type in 'post':
                self.response = self.session.post(url_path,
                                                params=fargs,
                                                headers=headers,
                                                auth=auth)
        except ConnectionError or MaxRetryError as e:
            msg = "[Error]: In Connection.make_request -> "\
                  "Could not establish the connection to "+url_path+"."
            self.output.error(msg)

            return ({}, False)

        status = self.response.status_code
        reason = self.response.reason

        if status != 200:
            msg = "[ERROR]: Connection.make_request() -> Unable to complete "\
                  "the request because -> "+str(reason)
            self.output.error(msg)
            return({}, False)


        if not expectResponse:
            return ({}, True)

        try:
            self.data = self.response.json()
        except (ValueError, json.decoder.JSONDecodeError) as e:
            msg = "[WARNING] in Connection -> Value Error "
            self.output.error(msg)
            self.output.error(str(e))
            if self.data == None and request_type == 'post':
                self.data = {}
            else:
                return (None, False)

        #print(self.response)

        return (self.data, True)
