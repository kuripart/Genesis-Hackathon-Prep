from .HTTPRequest import HTTPRequest
from .suffix_keys import url_suff as suff

# 6) TRAINING
# 6.1 Train a model
# 6.2 Response fields
# 6.3 View a trained model
# 6.4 View a list of trained models
# 6.5 Response fields

def train_model(server_name, url_suff, kbase_id, lang_code):

    full_addr = server_name + url_suff["train_model"]
    full_addr = full_addr.format(knowledgebaseID=kbase_id,
                                 languageCode=lang_code)

    req = HTTPRequest(full_addr, "POST")
    response = (req.post()).json()

    training_id = response["id"]

def view_trained_model(server_name, url_suff, kbase_id, lang_code,training_id):

    full_addr = server_name + url_suff["view_trained_model"]
    full_addr = full_addr.format(knowledgebaseID=kbase_id,
                                 languageCode=lang_code,
                                 trainingId=training_id)

    req = HTTPRequest(full_addr, "GET")
    response = req.get().json()


def view_trained_model_list(server_name, url_suff, kbase_id, lang_code,model_limit=1):

    full_addr = server_name + url_suff["view_trained_model_list"]
    full_addr = full_addr.format(knowledgebaseID=kbase_id,
                                 languageCode=lang_code,
                                 limit=model_limit)

    req = HTTPRequest(full_addr, "GET")
    response = (req.get())

    req_list = response.json()
