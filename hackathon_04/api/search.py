from HTTPRequest import HTTPRequest
from suffix_keys import url_suff as suff

payload_in = {
    "query": "",
    "pageSize": 3,
    "pageNumber": 1,
    "languageCode":"en-US",
    "documentType":"faq"
}


def search(server_name, url_suff, kbase_id, req_payload, org_id, token, search_size=1):

    full_addr = server_name + url_suff["search"]
    full_addr = full_addr.format(knowledgebaseId=kbase_id)

    req = HTTPRequest(full_addr, "POST")

    for key in req_payload.keys():
        req.payload_append(key,req_payload[key])
    req.payload_append("pageSize", search_size)
    req.payload_append("pageNumber", 1)
    req.payload_append("languageCode", "en-US")
    req.payload_append("documentType", "Faq")

    req.add_header("Content-Type", "application/json")
    req.add_header("organizationid", org_id)
    req.add_header("token", token)
    req.add_header("cache-control", "no-cache")

    response = (req.post())
    print("Response status: ", response.status_code)
    resp_json = response.json()
    results = resp_json["results"]

    return results