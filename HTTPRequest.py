# Authors: Nithin Prasad and Partha Sarathi Kuri
# Date Created: 12 October, 2019
# Program Name: hackathon_api.py
# Program Description: This program contains API calls and algorithms to handle and
# test the calls, to be implemented in the final hackathon project.


import requests
import suffix_keys.url_suff as suffs

server_name = "https://api.genesysapplkedresearch.com"  # Central Server


# Class to handle HTTP (Post/Get)
class HTTPRequest:
    url = None
    req_type = None
    data = {}  # Fill in with separate functions

    def __init__(self, url_in, req_type_in):

        self.url = url_in
        self.req_type = req_type_in

    def append(self, key, val):
        self.data[key] = val

    def post(self):
        if self.req_type != "POST":
            return "ERROR: Wrong request!"

        response = requests.post(url=self.url, data=self.data)

        return response

    def get(self):
        if self.req_type == "GET":
            return "ERROR: Wrong request!"

        response = requests.get(url=self.url, data=self.data)

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

    def delete(self):
        if self.req_type != "DELETE":
            return "ERROR: Wrong request!"

        response = requests.delete(url=self.url, data=self.data)

        return response
