from .HTTPRequest import HTTPRequest
from .suffix_keys import url_suff as suff


# 3) KNOWLEDGE BASES
# 3.1 Create a knowledge base
# 3.2 view a knowledge base
# 3.3 view a list of knowledge bases
# 3.4 update a knowledge base
# 3.5 delete a knowledge base


payload_info = {"name": None,
                "description": None,
                "coreLanguage": "en-US"}


# POST Request
def create_kbase(server_name, url_suff, payload_info, kbase_responses={}):

    # Check if # of databases exceeds limit (5)
    if len(kbase_responses.items()) == 5:
        return {},

    full_addr = server_name + url_suff["create_kbase"]

    req = HTTPRequest(full_addr, "POST")

    for key in payload_info.keys():
        req.payload_append(key, payload_info[key])

    response = req.post()

    resp_id = response.json().get("id")
    kbase_responses['status_code'] = response.status_code
    if resp_id:
        kbase_responses[resp_id] = (response["dateCreated"],
                                    response["dateModified"],
                                    response["selfUri"])
    else:
        return kbase_responses

    return kbase_responses


# GET Request
def view_kbase(server_name, url_suff, limit=1, kbase_id=None):
    full_addr = server_name + url_suff["view_kbase"]
    response_list = []
    if kbase_id:
        full_addr += kbase_id
        req = HTTPRequest(full_addr, "GET")
        response = req.get()
        response_dict = response.json()
        if response_dict.status_code == 200:
            response_list.append(response_dict)
    else:
        full_addr += '?limit={0}'.format(limit)
        req = HTTPRequest(full_addr, "GET")
        response = req.get()
        response_dict = response.json()
        if response.status_code == 200:
            response_list = [response_dict]
            while response_dict.get("nextUri", 'null') != 'null':
                full_addr = server_name + url_suff["view_kbase"]
                full_addr += '?limit={0}'.format(limit)
                full_addr += response_dict.get("nextUri")
                req = HTTPRequest(full_addr, "GET")
                response = req.get()
                response_dict = response.json()
                if response.status_code == 200:
                    response_list.append(response_dict)

    return response_list


# PUT Request
def update_kbase(server_name, url_suff, payload_info, kbase_id):
    full_addr = server_name + url_suff["update_kbase"]
    full_addr += kbase_id
    req = HTTPRequest(full_addr, "PUT")
    for key in payload_info.keys():
        req.payload_append(key, payload_info[key])
    response = req.put()
    response_result = response.json()
    response_result['status_code'] = response.status_code
    return response_result


# DELETE Request
def delete_kbase(server_name, url_suff, kbase_id):
    full_addr = server_name + url_suff["delete_kbase"]
    full_addr += kbase_id
    req = HTTPRequest(full_addr, "DELETE")
    response = req.delete()
    response_result = response.json()
    response_result['status_code'] = response.status_code
    return response_result

