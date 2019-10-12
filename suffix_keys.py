url_suff = {} #Contain all the URL suffixes for the API

#KNOWLEDGE BASE INTERACTION SUFFIXES
for key in ("create_kbase", "view_kbase", "update_kbase", "delete_kbase"):
    url_suff[key] = "/v2/knowledge/knowledgebases"