from HTTPRequest import HTTPRequest
from suffix_keys import url_suff as suff


# 5) DOCUMENTS
# 5.1 Upload a single document
# 5.2 Update/Upload multiple documents
# 5.3 Update a single document
# 5.4 View all documents
# 5.5 View a single document
# 5.6 Delete a document

doc_payload = {"question": "",
               "answer": "",
               "alternatives": ""}


def upload_doc(server_name, url_suff, kbase_id, lang_code, payload, categories={}):
    full_addr = server_name + url_suff["upload_doc"]
    full_addr = full_addr.format(knowledgebaseID=kbase_id,
                                 languageCode=lang_code)
    req = HTTPRequest(full_addr, "POST")
    req.payload_append("type", "Faq")
    key = "faq"
    val = {"question": payload["question"],
           "answer": payload["answer"],
           "alternatives": payload["alternatives"]}
    req.payload_append(key, val)
    key = "categories"
    val = []
    for elem1, elem2 in categories.items():
        val.append({elem1: elem2})
    req.payload_append(key, val)
    req.payload_append("externalUrl", "")
    response = req.post()
    return response.status_code


# Payload test for mod_docs fn
doc_payloads = [{"question": "", "answer": "", "alternatives": ""},
                {"question": "", "answer": "", "alternatives": ""},
                {"question": "", "answer": "", "alternatives": ""}]


def mod_docs(server_name, url_suff, kbase_id, lang_code, payloads, categories={}):
    full_addr = server_name + url_suff["mod_docs"]
    full_addr = full_addr.format(knowledgebaseID=kbase_id,
                                 languageCode=lang_code)
    responses = ()
    request_count = 0
    req = HTTPRequest(full_addr, "PATCH")

    for payload in payloads:
        request_count += 1
        req.payload_append("type", "Faq")
        key = "faq"
        val = {"question": payload["question"],
               "answer": payload["answer"],
               "alternatives": payload["alternatives"]}
        req.payload_append(key, val)
        key = "categories"
        val = []
        for elem1, elem2 in categories.items():
            val.append({elem1: elem2})
        req.payload_append(key, val)
        req.payload_append("externalUrl", "")
        response = req.patch()
        response_dict = response.json()
        responses += ((response_dict.get('id', request_count), response.status_code), )

    return responses


def update_doc(server_name, url_suff, kbase_id, lang_code, payload, doc_id, categories={}):
    full_addr = server_name + url_suff["update_doc"]
    full_addr = full_addr.format(knowledgebaseID=kbase_id,
                                 languageCode=lang_code,
                                 documentId=doc_id)
    req = HTTPRequest(full_addr, "PUT")
    req.payload_append("type", "Faq")
    key = "faq"
    val = {"question": payload["question"],
           "answer": payload["answer"],
           "alternatives": payload["alternatives"]}
    req.payload_append(key, val)
    key = "categories"
    val = []
    for elem1, elem2 in categories.items():
        val.append({elem1: elem2})
    req.payload_append(key, val)
    req.payload_append("externalUrl", "")
    response = req.put()
    return response.status_code


def view_doc(server_name, url_suff, kbase_id, lang_code, doc_id):
    full_addr = server_name + url_suff["view_doc"]
    full_addr = full_addr.format(knowledgebaseId=kbase_id,
                                 languageCode=lang_code,
                                 documentId=doc_id)
    req = HTTPRequest(full_addr, "GET")
    response_list = []
    response = req.get()
    if response.status_code == 200:
        response_list.append(response.json())
    return response_list


def view_docs(server_name, url_suff, kbase_id, lang_code, limit=1):
    full_addr = server_name + url_suff["view_docs"]
    full_addr += '?limit={limit_num}'
    full_addr = full_addr.format(knowledgebaseId=kbase_id,
                                 languageCode=lang_code,
                                 limit_num=limit)
    req = HTTPRequest(full_addr, "GET")
    response = req.get()
    response_dict = response.json()
    response_list = [response_dict]
    while response_dict.get("nextUri", 'null') != 'null':
        full_addr = server_name + url_suff["view_docs"]
        full_addr += '?limit={limit_num}'
        full_addr = full_addr.format(knowledgebaseId=kbase_id,
                                     languageCode=lang_code,
                                     limit_num=limit)
        full_addr += response["nextUri"]
        req = HTTPRequest(full_addr, "GET")
        response = req.get()
        response_dict = response.json()
        response_list.append(response_dict)

    return response_list


def delete_doc(server_name, url_suff, kbase_id, lang_code, doc_id):
    full_addr = server_name + url_suff["delete_doc"]
    full_addr = full_addr.format(knowledgebaseId=kbase_id,
                                 languageCode=lang_code,
                                 documentId=doc_id)
    req = HTTPRequest(full_addr, "DELETE")
    response = req.delete()
    return response.status_code
