url_suff = {} #Contain all the URL suffixes for the API

#KNOWLEDGE BASE INTERACTION SUFFIXES
for key in ("create_kbase", "view_kbase", "update_kbase", "delete_kbase"):
    url_suff[key] = "/v2/knowledge/knowledgebases"

url_suff["create_ctg"] = "/v2/knowledge/knowledgebases/{knowledgebaseId}/languages/{languageCode}/categories"
url_suff["view_ctg"] = "/v2/knowledge/knowledgebases/{knowledgebaseId}/languages/{languageCode}/categories"

for key in ("update_ctg", "delete_ctg"):
    url_suff[key] = "/v2/knowledge/knowledgebases/{knowledgebaseId}/languages/{languageCode}/categories/{categoryId}"

for key in ("upload_doc","mod_docs","view_doc"):
    url_suff[key] = "/api/v2/knowledge/knowledgebases/{knowledgebaseId}/language/{languageCode}/documents"

for key in ("update_doc","view_docs","delete_docs"):
    url_suff[key] = "/api/v2/knowledge/knowledgebases/{knowledgebaseId}/language/{languageCode}/documents/{documentId}"

