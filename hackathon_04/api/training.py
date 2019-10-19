from HTTPRequest import HTTPRequest
from suffix_keys import url_suff as suff

# 6) TRAINING
# 6.1 Train a model
# 6.2 Response fields
# 6.3 View a trained model
# 6.4 View a list of trained models
# 6.5 Response fields

def train_model(server_name, url_suff, kbase_id, lang_code, org_id, token):

    full_addr = server_name + url_suff["train_model"]
    full_addr = full_addr.format(knowledgebaseId=kbase_id,
                                 languageCode=lang_code)

    req = HTTPRequest(full_addr, "POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("organizationid", org_id)
    req.add_header("token", token)
    req.add_header("cache-control", "no-cache")
    response = req.post()
    response_dict = response.json()
    print(response.status_code)

    training_id = response_dict["id"]
    return (training_id)

def view_trained_model(server_name, url_suff, kbase_id, lang_code,training_id, org_id, token):

    full_addr = server_name + url_suff["view_trained_model"]
    full_addr = full_addr.format(knowledgebaseId=kbase_id,
                                 languageCode=lang_code,
                                 trainingId=training_id)

    req = HTTPRequest(full_addr, "GET")

    req.add_header("Content-Type", "application/json")
    req.add_header("organizationid", org_id)
    req.add_header("token", token)
    req.add_header("cache-control", "no-cache")
    response = req.get()
    print(response.status_code)
    resp_json = response.json()

    return resp_json["status"]




def view_trained_model_list(server_name, url_suff, kbase_id, lang_code,model_limit=1):

    full_addr = server_name + url_suff["view_trained_model_list"]
    full_addr = full_addr.format(knowledgebaseId=kbase_id,
                                 languageCode=lang_code,
                                 limit=model_limit)

    req = HTTPRequest(full_addr, "GET")
    response = (req.get())

    req_list = response.json()
