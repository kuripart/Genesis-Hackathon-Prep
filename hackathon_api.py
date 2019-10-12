#Authors: Nithin Prasad and Partha Sarathy Kuri
#Date Created: 12 October, 2019
#Program Name: hackathon_api.py
#Program Description: This program contains API calls and algorthms to handle and
# test the calls, to be implemented in the final hackthon project.

import requests

#Class to handle HTTP (Post/Get)
class HTTP_Request:

    url = None
    req_type = None
    data = {} #Fill in with separate functions
    
    def __init__(self, url_in, req_type_in):
        
        self.url = url_in
        self.req_type = req_type_in

    def req_append(self,key,val):

        self.data[key] = val

    def post(self):

        if self.req_type == "GET":

            return "ERROR: Wrong request!"

        response = requests.post(url = self.url, data = self.data)

        return response

    def get(self):

        if self.req_type == "POST":

            return "ERROR: Wrong request!"

        response = requests.get(url = self.url, data = self.data)

        return response

###################################################################
class HTTP_Request:

    url = None
    req_type = None
    data = {} #Fill in with separate functions
    
    def __init__(self, url_in, req_type_in):
        
        self.url = url_in
        self.req_type = req_type_in

    def append(self,key,val):

        self.data[key] = val

    def post(self):

        if self.req_type == "GET":

            return "ERROR: Wrong request!"

        response = requests.post(url = self.url, data = self.data)

        return response

    def get(self):

        if self.req_type == "POST":

            return "ERROR: Wrong request!"

        response = requests.get(url = self.url, data = self.data)

        return response

#Tasks to accomplish:
########### 3) KNOWLEDGE BASES ###########
#3.1 Create a knowledge base
#3.2 view a knowledge base
#3.3 view a list of knowledge bases
#3.4 update a knowledge base
#3.5 delete a knowledge base

server_name = "https://api.genesysapplkedresearch.com" #Central Server

url_suff = {} #Contain all the URL suffixes for the API

#KNOWLEDGE BASE INTERACTION SUFFIXES
url_suff["create_kbase"] = "/v2/knowledge/knowledgebases" #POST

kbase_responses = {}

payload_info = {"name":None,
                "description":None,
                "coreLanguage":"en-US"}

#POST Request
def create_kbase(server_name, url_suff, payload_info, kbase_responses):
    '''
    server_name <= string, represents Genesys central API server
    url_suff <= dict, knowledge base API url tags
    payload_info <= dict, keys: name (of K_base), description, coreLanguage

    kbase_responses => dict, key
    '''

    #Check if # of databases exceeds limit (5)
    if len(kbase_responses.items()) == 5:
        return False

    full_addr = server_name + url_suff["create_kbase"]
    
    req = HTTP_Request(full_addr, "POST")

    for key in payload_info.keys():
        req.append(key,payload_info[key])

    response = req.post()

    resp_id = response["id"]
    kbase_responses[resp_id] = (response["dateCreated"],
                                response["dateModified"],
                                response["selfUri"])

    return True

#global test_dict
test_dict = {}
print("PRE: ", test_dict)

def test(test_dict_in):
    
    print("In fn, pre: ", test_dict_in)
    test_dict_in["alpha"] = "gamma"
    print("In fn, post: ", test_dict_in)

    return

test(test_dict)
print("POST: ", test_dict)


    
    





    

    

    
    

    
