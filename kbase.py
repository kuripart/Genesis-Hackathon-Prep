from HTTPRequest import HTTPRequest
import suffix_keys.url_suff as suffs


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
def create_kbase(server_name, url_suff, payload_info, kbase_responses):

    # Check if # of databases exceeds limit (5)
    if len(kbase_responses.items()) == 5:
        return False

    full_addr = server_name + url_suff["create_kbase"]

    req = HTTPRequest(full_addr, "POST")

    for key in payload_info.keys():
        req.append(key, payload_info[key])

    response = req.post()

    resp_id = response["id"]
    kbase_responses[resp_id] = (response["dateCreated"],
                                response["dateModified"],
                                response["selfUri"])

    return True


# GET Request
def view_kbase(server_name, url_suff, limit=1, kbase_id=None):
    full_addr = server_name + url_suff["view_kbase"]
    if kbase_id:
        full_addr += kbase_id
        req = HTTPRequest(full_addr, "GET")
        response = req.get()

    else:
        full_addr += '?limit={0}'.format(limit)
        req = HTTPRequest(full_addr, "GET")
        response = req.get()
        response_list = [response]
        while response["nextUri"] != 'null':
            full_addr = server_name + url_suff["view_kbase"]
            full_addr += '?limit={0}'.format(limit)
            full_addr += response["nextUri"]
            req = HTTPRequest(full_addr, "GET")
            response = req.get()
            response_list.append(response)


# PUT Request
def update_kbase(kbase_id, server_name, url_suff, limit=None):
    full_addr = server_name + url_suff["update_kbase"]
    full_addr += kbase_id
    req = HTTPRequest(full_addr, "PUT")
    response = req.put()


# DELETE Request
def delete_kbase(kbase_id, server_name, url_suff, limit=None):
    full_addr = server_name + url_suff["delete_kbase"]
    full_addr += kbase_id
    req = HTTPRequest(full_addr, "DELETE")
    response = req.put()  # This could be req.delete()

