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

    def patch(self):
        if self.req_type != "PATCH":
            return "ERROR: Wrong request!"

        response = requests.patch(url=self.url, data=self.data)


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
def view_kbase(server_name, url_suff, limit=1, kbase_id=None):
    full_addr = server_name + url_suff["view_kbase"]
    if kbase_id:
        full_addr += kbase_id
        req = HTTP_Request(full_addr, "GET")
        response = req.get()

    else:
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
#4.1 Create a category
#4.2 view a list of categories
#4.3 view a category
#4.4 update a category
#4.5 delete a category

payload_info_ctg = {"name":None,
                    "description":None}

kbase_categories = {}

#PUT Request
def create_ctg(server_name, url_suff, payload_info_ctg, kbase_id, lang_code):
    full_addr = server_name + url_suff["create_ctg"]
    full_addr = full_addr.format(knowledgebaseId = kbase_id, languageCode = lang_code)

    req = HTTP_Request(full_addr, "POST")

    for key in payload_info_ctg.keys():
        req.append(key, payload_info_ctg[key])

    response = req.post()

    resp_kbase_id = response["knowledgeBase"]["id"]
    ctg = response["id"]

    if resp_kbase_id in kbase_categories.keys():
        kbase_responses[resp_kbase_id].append(ctg)
    else:
        kbase_responses[resp_kbase_id] = [ctg]

def view_ctg(server_name, url_suff, kbase_id, lang_code, ctg_id=None, limit=1):
    full_addr = server_name + url_suff["view_ctg"]
    if ctg_id:
        full_addr += '/{categoryId}'
        full_addr = full_addr.format(knowledgebaseId=kbase_id,
                                     languageCode=lang_code,
                                     categoryId=ctg_id)
        req = HTTP_Request(full_addr, "GET")
        response = req.get()

    else:
        # if there is a limit, limit your request
        full_addr += '?limit={limit_num}'
        full_addr = full_addr.format(knowledgebaseId=kbase_id,
                                     languageCode=lang_code,
                                     categoryId=ctg_id,
                                     limit_num = limit)
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

######################################################################
########### 4) DOCUMENTS ###########
#5.1 Upload a single document
#5.2 Update/Upload multiple documents
#5.3 Update a single document
#5.4 View all documents
#5.5 View a single document
#5.6 Delete a document

doc_payload = {"question":"",
               "answer":"",
               "alternatives":""}

def upload_doc(server_name, url_suff, kbase_id, lang_code, payload,
               categories = {}):

    full_addr = server_name + url_suff["upload_doc"]
    full_addr = full_addr.format(knowledgebaseID = kbase_id,
                                 languageCode = lang_code)
    
    req = HTTP_Request(full_addr, "POST")

    req.append("type","Faq")
    key = "faq"
    val = {"question": payload["question"],
           "answer":payload["answer"],
           "alternatives":payload["alternatives"] }
    req.append(key,val)
    key = "categories"
    val = []
    for elem1,elem2 in categories.items():
        val.append({elem1:elem2})
    req.append(key,val)
    req.append("externalUrl", "string")

    response = req.post()

#Payload test for mod_docs fn
doc_payloads = [{"question":"","answer":"","alternatives":""},
                {"question":"","answer":"","alternatives":""},
                {"question":"","answer":"","alternatives":""}]

def mod_docs(server_name, url_suff, kbase_id, lang_code, payloads,
             categories = {}):

    full_addr = server_name + url_suff["upload_doc"]
    full_addr = full_addr.format(knowledgebaseID = kbase_id,
                                 languageCode = lang_code)
    
    req = HTTP_Request(full_addr, "PATCH")

    for payload in payloads:
        
        req.append("type","Faq")
        key = "faq"
        val = {"question": payload["question"],
               "answer":payload["answer"],
               "alternatives":payload["alternatives"] }
        req.append(key,val)
        key = "categories"
        val = []
        for elem1,elem2 in categories.items():
            val.append({elem1:elem2})
        req.append(key,val)
        req.append("externalUrl", "string")

        response = req.patch()

def update_doc(server_name, url_suff, kbase_id, lang_code, payload,
               doc_id, categories = {}):

    full_addr = server_name + url_suff["update_doc"]
    full_addr = full_addr.format(knowledgebaseID = kbase_id,
                                 languageCode = lang_code,
                                 documentId = doc_id)
    
    req = HTTP_Request(full_addr, "PUT")

    req.append("type","Faq")
    key = "faq"
    val = {"question": payload["question"],
           "answer":payload["answer"],
           "alternatives":payload["alternatives"] }
    req.append(key,val)
    key = "categories"
    val = []
    for elem1,elem2 in categories.items():
        val.append({elem1:elem2})
    req.append(key,val)
    req.append("externalUrl", "string")

    response = req.put()

def view_doc(server_name, url_suff, kbase_id, lang_code, doc_id):

    pass

def view_docs(server_name, url_suff, kbase_id, lang_code):

    pass

def delete_doc(server_name, url_suff, kbase_id, lang_code, doc_id):

    pass

    











