# Authors: Nithin Prasad and Partha Sarathi Kuri
# Date Created: 12 October, 2019
# Program Name: hackathon_api.py
# Program Description: This program contains API calls and algorithms to handle and
# test the calls, to be implemented in the final hackathon project.


import requests
from suffix_keys import url_suff as suff
<<<<<<< HEAD
import json
=======
>>>>>>> fd1799c14c2e68c12f1b4bc512c9aab808d37bd6

server_name = "https://api.genesysappliedresearch.com"  # Central Server


# Class to handle HTTP (Post/Get)
class HTTPRequest:
    url = None
    req_type = None
    headers = {}
    data = {}  # Fill in with separate functions

    def __init__(self, url_in, req_type_in):

        self.url = url_in
        self.req_type = req_type_in

    def payload_append(self, key, val):
        self.data[key] = val

    def add_header(self, key, val):
        self.headers[key] = val

    def post(self):
        if self.req_type != "POST":
            return "ERROR: Wrong request!"

        print("Request URL: ",self.url)
        print("Data: ",self.data)
        print("Headers: ",self.headers)

        data_dumps = json.dumps(self.data)
        #headers_dumps = json.dumps(self.headers)
        #print("Data_dumps: ", data_dumps)
        #print("Headers_dumps",headers_dumps)
        response = requests.post(url=self.url, data=data_dumps, headers=self.headers)


        return response

    def get(self):
        if self.req_type != "GET":
            return "ERROR: Wrong request!"
        data_dumps = json.dumps(self.data)

        print("Request URL: ",self.url)
        print("Data: ",self.data)
        print("Headers: ",self.headers)
        response = requests.get(url=self.url, data=self.data, headers=self.headers)

        return response

    def put(self):
        if self.req_type != "PUT":
            return "ERROR: Wrong request!"

        response = requests.put(url=self.url, data=self.data)

        return response

    def patch(self):
        if self.req_type != "PATCH":
            return "ERROR: Wrong request!"

        response = requests.patch(url=self.url, data=self.data)

        return response

    def delete(self):
        if self.req_type != "DELETE":
            return "ERROR: Wrong request!"

        response = requests.delete(url=self.url, data=self.data)

        return response
