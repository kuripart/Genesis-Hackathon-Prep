from .HTTPRequest import HTTPRequest
from .suffix_keys import url_suff as suff

payload_in = {
    "query": "",
    "pageSize": 3,
    "pageNumber": 1,
    "languageCode":"en-US",
    "documentType":"faq"
}

def search(server_name, url_suff, kbase_id, req_payload):

    full_addr = server_name + url_suff["search"]
    full_addr = full_addr.format(knowledgebaseID=kbase_id)

    req = HTTPRequest(full_addr, "POST")

    for key in req_payload.keys():
        req.payload_append(key,req_payload[key])

    response = (req.post()).json()

    training_id = response["id"]