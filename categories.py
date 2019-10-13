from HTTPRequest import HTTPRequest
from suffix_keys import url_suff as suff


# 4) CATEGORIES
# 4.1 Create a category
# 4.2 view a list of categories
# 4.3 view a category
# 4.4 update a category
# 4.5 delete a category

payload_info_ctg = {"name": None,
                    "description": None}

kbase_responses = {}
kbase_categories = {}


# PUT Request
def create_ctg(server_name, url_suff, payload_info_ctg, kbase_id, lang_code):
    full_addr = server_name + url_suff["create_ctg"]
    full_addr = full_addr.format(knowledgebaseId=kbase_id, languageCode=lang_code)

    req = HTTPRequest(full_addr, "POST")

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
        req = HTTPRequest(full_addr, "GET")
        response = req.get()

    else:
        # if there is a limit, limit your request
        full_addr += '?limit={limit_num}'
        full_addr = full_addr.format(knowledgebaseId=kbase_id,
                                     languageCode=lang_code,
                                     categoryId=ctg_id,
                                     limit_num = limit)
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


def update_ctg(server_name, url_suff, kbase_id, lang_code, ctg_id):

    full_addr = server_name + url_suff["update_ctg"]
    full_addr = full_addr.format(knowledgebaseId=kbase_id,
                                 languageCode=lang_code,
                                 categoryId=ctg_id)
    req = HTTPRequest(full_addr, "PUT")
    response = req.put()


def delete_ctg(server_name, url_suff, kbase_id, lang_code, ctg_id):

    full_addr = server_name + url_suff["delete_ctg"]
    full_addr = full_addr.format(knowledgebaseId=kbase_id,
                                 languageCode=lang_code,
                                 categoryId=ctg_id)
    req = HTTPRequest(full_addr, "DELETE")
    response = req.put()  # This could be req.delete()
