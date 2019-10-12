#Authors: Nithin Prasad and Partha Sarathy Kuri
#Date Created: 12 October, 2019
#Program Name: hackathon_api.py
#Program Description: This program contains API calls and algorthms to handle and
# test the calls, to be implemented in the final hackthon project.

import requests
import suffix_keys.url_suff as suffs

#Class to handle HTTP (Post/Get)
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

        if self.req_type != "POST":

            return "ERROR: Wrong request!"

        response = requests.post(url = self.url, data = self.data)

        return response

    def get(self):

        if self.req_type == "GET":

            return "ERROR: Wrong request!"

        response = requests.get(url = self.url, data = self.data)

        return response

    def put(self):
        if self.req_type != "PUT":
            return "ERROR: Wrong request!"

        response = requests.put(url=self.url, data=self.data)

        return response


    def delete(self):
        if self.req_type != "DELETE":
            return "ERROR: Wrong request!"

        response = requests.delete(url=self.url, data=self.data)

        return response

#Tasks to accomplish:
########### 3) KNOWLEDGE BASES ###########
#3.1 Create a knowledge base
#3.2 view a knowledge base
#3.3 view a list of knowledge bases
#3.4 update a knowledge base
#3.5 delete a knowledge base

server_name = "https://api.genesysapplkedresearch.com" #Central Server

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
    :return True if successful False if not
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


#GET Request
def view_kbase(server_name, url_suff, limit=None, kbase_id=None):
    full_addr = server_name + url_suff["view_kbase"]
    if kbase_id:
        full_addr += kbase_id
        req = HTTP_Request(full_addr, "GET")
        response = req.get()

    else:
        # if there is a limit, limit your request
        if limit:
            full_addr += '?limit={0}'.format(limit)
            req = HTTP_Request(full_addr, "GET")
            response = req.get()
            response_list = []
            response_list.append(response)
            while response["nextUri"] != 'null':
                full_addr = server_name + url_suff["view_kbase"]
                full_addr += '?limit={0}'.format(limit)
                full_addr += response["nextUri"]
                req = HTTP_Request(full_addr, "GET")
                response = req.get()
                response_list.append(response)

    req = HTTP_Request(full_addr, "GET")

    response = req.get()

#PUT Request
def update_kbase(kbase_id, server_name, url_suff, limit=None):
    full_addr = server_name + url_suff["update_kbase"]
    full_addr += kbase_id
    req = HTTP_Request(full_addr, "PUT")
    response = req.put()

#DELETE Request
def delete_kbase(kbase_id, server_name, url_suff, limit=None):
    full_addr = server_name + url_suff["delete_kbase"]
    full_addr += kbase_id
    req = HTTP_Request(full_addr, "DELETE")
    response = req.put() # This could be req.delete()

######################################################################
########### 3) CATEGORIES ###########
#3.1 Create a category
#3.2 view a list of categories
#3.3 view a category
#3.4 update a category
#3.5 delete a category

#PUT Request
def create_ctg():

    pass

def view_ctg():

    pass

def update_ctg(server_name, url_suff, kbase_id, lang_code, ctg_id):

    full_addr = server_name + url_suff["update_ctg"]
    full_addr = full_addr.format(knowledgebaseId = kbase_id,
                                 languageCode = lang_code,
                                 categoryId = ctg_id)
    req = HTTP_Request(full_addr, "PUT")
    response = req.put()

def delete_ctg(server_name, url_suff, kbase_id, lang_code, ctg_id):

    full_addr = server_name + url_suff["delete_ctg"]
    full_addr = full_addr.format(knowledgebaseId = kbase_id,
                                 languageCode = lang_code,
                                 categoryId = ctg_id)
    req = HTTP_Request(full_addr, "DELETE")
    response = req.put() #This could be req.delete()







