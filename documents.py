from HTTPRequest import HTTPRequest
import suffix_keys.url_suff as suffs


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

    req.append("type", "Faq")
    key = "faq"
    val = {"question": payload["question"],
           "answer": payload["answer"],
           "alternatives": payload["alternatives"]}
    req.append(key, val)
    key = "categories"
    val = []
    for elem1, elem2 in categories.items():
        val.append({elem1: elem2})
    req.append(key, val)
    req.append("externalUrl", "string")

    response = req.post()


# Payload test for mod_docs fn
doc_payloads = [{"question": "", "answer": "", "alternatives": ""},
                {"question": "", "answer": "", "alternatives": ""},
                {"question": "", "answer": "", "alternatives": ""}]


def mod_docs(server_name, url_suff, kbase_id, lang_code, payloads, categories={}):
    full_addr = server_name + url_suff["upload_doc"]
    full_addr = full_addr.format(knowledgebaseID=kbase_id,
                                 languageCode=lang_code)

    req = HTTPRequest(full_addr, "PATCH")

    for payload in payloads:

        req.append("type", "Faq")
        key = "faq"
        val = {"question": payload["question"],
               "answer": payload["answer"],
               "alternatives": payload["alternatives"]}
        req.append(key, val)
        key = "categories"
        val = []
        for elem1, elem2 in categories.items():
            val.append({elem1: elem2})
        req.append(key, val)
        req.append("externalUrl", "string")

        response = req.patch()


def update_doc(server_name, url_suff, kbase_id, lang_code, payload, doc_id, categories={}):
    full_addr = server_name + url_suff["update_doc"]
    full_addr = full_addr.format(knowledgebaseID=kbase_id,
                                 languageCode=lang_code,
                                 documentId=doc_id)

    req = HTTPRequest(full_addr, "PUT")

    req.append("type", "Faq")
    key = "faq"
    val = {"question": payload["question"],
           "answer": payload["answer"],
           "alternatives": payload["alternatives"]}
    req.append(key, val)
    key = "categories"
    val = []
    for elem1, elem2 in categories.items():
        val.append({elem1: elem2})
    req.append(key, val)
    req.append("externalUrl", "string")

    response = req.put()


def view_doc(server_name, url_suff, kbase_id, lang_code, doc_id):
    full_addr = server_name + url_suff["view_doc"]
    full_addr = full_addr.format(knowledgebaseId=kbase_id,
                                 languageCode=lang_code,
                                 documentId=doc_id)

    req = HTTPRequest(full_addr, "GET")
    response = req.get()


def view_docs(server_name, url_suff, kbase_id, lang_code, limit=1):
    full_addr = server_name + url_suff["view_docs"]
    full_addr += '?limit={limit_num}'
    full_addr = full_addr.format(knowledgebaseId=kbase_id,
                                 languageCode=lang_code,
                                 limit_num=limit)
    req = HTTPRequest(full_addr, "GET")
    response = req.get()
    response_list = [response]
    while response["nextUri"] != 'null':
        full_addr = server_name + url_suff["view_docs"]
        full_addr += '?limit={limit_num}'
        full_addr = full_addr.format(knowledgebaseId=kbase_id,
                                     languageCode=lang_code,
                                     limit_num=limit)
        full_addr += response["nextUri"]
        req = HTTPRequest(full_addr, "GET")
        response = req.get()
        response_list.append(response)


def delete_doc(server_name, url_suff, kbase_id, lang_code, doc_id):
    full_addr = server_name + url_suff["delete_docs"]
    full_addr = full_addr.format(knowledgebaseId=kbase_id,
                                 languageCode=lang_code,
                                 documentId=doc_id)
    req = HTTPRequest(full_addr, "DELETE")
    response = req.put()  # This could be req.delete()
