from HTTPRequest import HTTPRequest
from suffix_keys import url_suff as suff

import requests
import json
import categories
import documents
import kbase
import training
import search
import time
import tkinter
import os

kbase_list = []


def manual_update(server_name, suff, org_id, token, kbase_list, lang_code, limit=5):
    payload_info = {"name": "Geography KBase",
                                    "description": "Template: First 20 Questions Tested for the Geography KBase",
                                    "coreLanguage": "en-US"}
    kbase_responses = {}

    # print("---------------------VIEWING KBASES----------------------")
    # kbase_list = view_kbases(server_name, suff, org_id, token, limit=limit)
    # print('kbase List Before Demolition', kbase_list)
    # print("---------------------DELETING ALL KBASES----------------------")
    # remove_all_kbases(org_id, token, server_name, suff, kbase_list)

    # print("---------------------VIEWING KBASES----------------------")
    # resp_list = view_kbases(server_name, suff, org_id, token, limit=limit)
    # print('Resp List After Demolition: ', resp_list)

    # print("---------------------CREATING KBASE----------------------")
    # kbase.create_kbase(server_name, suff, payload_info, org_id, token, kbase_responses)
    #
    print("---------------------VIEWING KBASES----------------------")
    kbase_list = view_kbases(server_name, suff, org_id, token, limit=limit)
    kbase_id1 = kbase_list[0]

    #------QA LOAD CODE----------
    q_fname = "questions_geography.txt"
    a_fname = "answers_geography.txt"
    batch_size = 25

    batch_size_list,batch_start_indices = compute_batches(q_fname, batch_size)
    #q_lines = None
    #a_lines = None
    #
    # print("------------------------------PRE-BATCH----------------------")
    # print("batch_size_list",batch_size_list)
    # print("batch_start_indices",batch_start_indices)
    #
    # for i in range(len(batch_size_list)):
    #     token = check_token_age('token_info.txt', org_id, client_secret)
    #
    #
    #     print("Processing Batch with start index: ", batch_start_indices[i], "||| Batch Size: ", batch_size_list[i])
    #     q_lines,a_lines = upload_knowledge_batch(q_fname, a_fname, batch_start_indices[i], batch_size_list[i], server_name, suff, kbase_id1, lang_code,
    #                        org_id, token)
    #
    #     train_in_batch(server_name, suff, kbase_id1, lang_code, org_id, token)

    print("---------------------TESTING MODEL ACCURACY-------------------")
    q_lines, a_lines = process_qa_txt_files(q_fname, a_fname)
    search_count = 0
    count_correct = 0
    results_list = []
    for i in range(len(q_lines)):
        question = q_lines[i].strip()
        answer = a_lines[i].strip()
        payload = {"query": question}
        results = search.search(server_name, suff, kbase_id1, payload, org_id, token)

        if results:
            result = results[0]["faq"]["answer"]
            print('result', result)
            print('answer', answer)
            print('result equality', result == answer)

            if result == answer.strip():
                count_correct += 1
        results_list.append(result)

        search_count += 1

    with open("query_validation.txt","w") as file:
        out_string = "OUTPUT FORMAT: <Answer>,<Result>,<Question>"
        file.write(out_string)
        for i in range(len(results_list)):
            out_string = a_lines[i].rstrip() + ", " + results_list[i].rstrip() + ", " + q_lines[i].rstrip() + "\n"
            file.write(out_string)
    print("Num Questions: ", search_count, "Num correct: ", count_correct)
    print("Model Accuracy: ", str((count_correct/search_count)*100))

# ---------------------VIEWING KBASES----------------------<FAILURE CASE>
# kbase_id in view_kbase None
# Request URL:  https://api.genesysappliedresearch.com/v2/knowledge/knowledgebases?limit=5
# Data:  {'name': 'Sample KBase', 'description': 'Testing our preliminary kbase!', 'coreLanguage': 'en-US'}
# Headers:  {'Content-Type': 'application/json', 'organizationid': '3ae6bd8b-23b6-47c7-a9a0-8dc56833ca18', 'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcmdJZCI6IjNhZTZiZDhiLTIzYjYtNDdjNy1hOWEwLThkYzU2ODMzY2ExOCIsImV4cCI6MTU3MTUzNTMwNywiaWF0IjoxNTcxNTMxNzA3fQ.6R1qMy6BeFoxJqO9s-yg5X9F8iR-GRoDXR4S1t8cti0', 'cache-control': 'no-cache'}
# Response: <Response [403]>

# ---------------------VIEWING KBASES----------------------
# kbase_id in view_kbase None
# Request URL:  https://api.genesysappliedresearch.com/v2/knowledge/knowledgebases?limit=5
# Data:  {}
# Headers:  {'Content-Type': 'application/json', 'organizationid': '3ae6bd8b-23b6-47c7-a9a0-8dc56833ca18', 'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcmdJZCI6IjNhZTZiZDhiLTIzYjYtNDdjNy1hOWEwLThkYzU2ODMzY2ExOCIsImV4cCI6MTU3MTUzNTMwNywiaWF0IjoxNTcxNTMxNzA3fQ.6R1qMy6BeFoxJqO9s-yg5X9F8iR-GRoDXR4S1t8cti0', 'cache-control': 'no-cache'}
# Response: <Response [200]>


def view_kbases(server_name, suff, org_id, token, limit=5):
    # VIEW Knowledge-Base
    resp_list = kbase.view_kbase(server_name, suff, org_id, token, limit=limit)
    return resp_list

def process_qa_txt_files(file_q_name, file_a_name):
    q_lines = []
    a_lines = []
    with open(file_q_name, 'r') as file_q:
        q_lines = file_q.readlines()

    with open(file_a_name, 'r') as file_a:
        a_lines = file_a.readlines()

    return (q_lines, a_lines)

def remove_all_kbases(org_id, token, server_name, suff, kbase_list):
    print("kbase_list", kbase_list)
    for kbase_id in kbase_list:
        remove_kbase(org_id, token, server_name, suff, kbase_id)

def remove_kbase(org_id, token, server_name, suff, kbase_id):
    kbase.delete_kbase(org_id, token, server_name, suff, kbase_id)

def compute_batches(fname, batch_size):

    batch_size_list = []
    batch_start_indices = []
    curr = 0

    with open(fname,"r") as file:
        file_size = len(file.readlines())
        while file_size-curr >= batch_size:
            batch_start_indices.append(curr)
            curr += batch_size
            batch_size_list.append(batch_size)
        if curr%batch_size != 0:
            batch_start_indices.append(curr)
            batch_size_list.append(file_size-curr)

    return (batch_size_list,batch_start_indices)

def upload_knowledge_batch(q_fname,a_fname,line_start_index,num_items,server_name,suff,kbase_id1,lang_code,org_id,token):
    print("---------------------PROCESSING QA FILES----------------------")
    q_lines, a_lines = process_qa_txt_files(q_fname, a_fname)

    print("---------------------UPLOADING QA TO KBASE----------------------")

    print("Num items in dict: ",len(q_lines))
    count = line_start_index
    line_end_index = line_start_index + num_items
    print("Count (start) = Line Start Index: ",count)
    print("Line End Index: ", line_end_index)
    for i in range(line_start_index, line_end_index):
        question = q_lines[i].strip()
        answer = a_lines[i].strip()
        payload = {"question":question,"answer":answer}
        documents.upload_doc(server_name, suff, kbase_id1, lang_code, payload, org_id, token, categories={})
        count += 1
        if count >= line_end_index:
            print("BREAKING! Count: ",count,"||| Line_End_Index: ",line_end_index)
            break
    print("NUM UPLOADS:",count-line_start_index)

    return q_lines, a_lines #Return lists of uploaded questions & answers!

def train_in_batch(server_name,suff,kbase_id1,lang_code,org_id,token):

    training_id_fname = "training_ids.txt"

    print("---------------------TRAINING KBASE----------------------")
    training_id = training.train_model(server_name, suff, kbase_id1, lang_code, org_id, token)
    print(training_id)


    out_string = training_id + "\n"
    if not os.path.exists(training_id_fname):
        print("Case 1")
        with open(training_id_fname, 'w') as file:
            file.write(out_string)
    else:
        with open(training_id_fname, 'a') as file:
            file.write(out_string)

    status_code = ""
    while status_code.lower() != "succeeded":
        print("---------------------VIEW TRAINING STATUS-------------------")
        resp_json = training.view_trained_model(server_name, suff, kbase_id1, lang_code, training_id, org_id, token)
        status_code = resp_json["status"].lower()
        if status_code == 'failed':
            print("resp_json: ", resp_json)
            print("status_code: ", status_code)
            print("errorMessage: ", resp_json["errorMessage"])
            error_message = resp_json["errorMessage"]
            index_words = error_message.index("-words")
            index_start = index_words + len("-words")
            substr_doc_id = error_message[index_start:]

            resp_doc = documents.view_doc(server_name, suff, kbase_id1, lang_code, substr_doc_id, org_id, token)
            print("Document failed question: ", resp_doc["faq"]["question"])
            print("Document failed answer: ", resp_doc["faq"]["answer"])

            return
        else:
            print("status_code: ", status_code)
        time.sleep(10)

def get_new_token(file, org_id, client_secret):
    headers = {
        'organizationid': org_id,
        'secretkey': client_secret,
    }

    payload_info = {"name": 'Token-Generator',
                    "description": 'Generate tokens for application',
                    "coreLanguage": "en-US"}

    data = json.dumps(payload_info)

    resp = requests.post('https://api.genesysappliedresearch.com/v2/knowledge/generatetoken', headers=headers, data=data)
    token_dict = resp.json()
    token = token_dict['token']
    start_time = time.time()
    file.write(str(start_time) + '\n')
    file.write(str(token))

    return token

def check_token_age(filename, org_id, client_secret):
    if not os.path.exists(filename):
        print("Case 1")
        with open(filename, 'w') as file:
            token = get_new_token(file, org_id, client_secret)
    else:
        rewrite_file = False
        token = ''
        with open(filename, 'r') as file:
            lines = file.readlines()
            token = lines[1]
            cur_time = time.time()
            hours, seconds = divmod(cur_time - float(lines[0]), 1800)
            if hours >= 1:
                print("Case 2")
                rewrite_file = True
            else:
                print("Case 3")

        if rewrite_file:
            with open(filename, 'w') as file:
                token = get_new_token(file, org_id, client_secret)

    return token

#SUCCESS CASE
# Request URL:  https://api.genesysappliedresearch.com/v2/knowledge/knowledgebases/e7bb5f8b-ec7a-441d-91b5-4c27386fb468/languages/en-US/documents
# Data:  {'type': 'faq', 'faq': {'question': 'Which state is the Lake Winnebago situated?', 'answer': 'Wisconsin.', 'alternatives': []}, 'categories': [], 'externalUrl': ''}
# Headers:  {'Content-Type': 'application/json', 'organizationid': '3ae6bd8b-23b6-47c7-a9a0-8dc56833ca18', 'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcmdJZCI6IjNhZTZiZDhiLTIzYjYtNDdjNy1hOWEwLThkYzU2ODMzY2ExOCIsImV4cCI6MTU3MTU0MzMxMiwiaWF0IjoxNTcxNTM5NzEyfQ.l50MeZ4dDVIUzNJ7nMCUTG6-OaBNzikHhuZ_wE65h44', 'cache-control': 'no-cache'}
# RESPONSE CODE:  200
# RESPONSE JSON:  {'id': '01a79352-88d3-4aeb-8dad-1b556868a8a8', 'type': 'faq', 'languageCode': 'en-US', 'article': None, 'faq': {'question': 'Which state is the Lake Winnebago situated?', 'answer': 'Wisconsin.', 'alternatives': []}, 'categories': [], 'knowledgeBase': {'id': 'e7bb5f8b-ec7a-441d-91b5-4c27386fb468', 'name': 'Geography KBase', 'description': 'Template: First 20 Questions Tested for the Geography KBase', 'coreLanguage': 'en-US', 'dateCreated': '2019-10-20T03:14:02.122Z', 'dateModified': '2019-10-20T03:14:02.122Z', 'selfUri': None}, 'externalUrl': '', 'selfUri': None, 'dateCreated': '2019-10-20T03:14:02.895Z', 'dateModified': '2019-10-20T03:14:02.895Z'}


#FAILURE CASE
# Request URL:  https://api.genesysappliedresearch.com/v2/knowledge/knowledgebases/e7bb5f8b-ec7a-441d-91b5-4c27386fb468/languages/en-US/documents
# Data:  {'type': 'faq', 'faq': {'question': "What's the smallest state of the U.S.", 'answer': 'Rhode Island', 'alternatives': []}, 'categories': [], 'externalUrl': ''}
# Headers:  {'Content-Type': 'application/json', 'organizationid': '3ae6bd8b-23b6-47c7-a9a0-8dc56833ca18', 'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcmdJZCI6IjNhZTZiZDhiLTIzYjYtNDdjNy1hOWEwLThkYzU2ODMzY2ExOCIsImV4cCI6MTU3MTU0MzMxMiwiaWF0IjoxNTcxNTM5NzEyfQ.l50MeZ4dDVIUzNJ7nMCUTG6-OaBNzikHhuZ_wE65h44', 'cache-control': 'no-cache'}
# RESPONSE CODE:  400
# RESPONSE JSON:  {'status': 400, 'code': '400', 'entityName': 'Document', 'message': 'Document with question Whats the smallest state of the U.S. already exists', 'messageWithParams': "Document with question What's the smallest state of the U.S. already exists", 'messageParams': {}, 'contextId': None, 'details': None}



if __name__ == "__main__":
    server_name = "https://api.genesysappliedresearch.com"
    org_id = "3ae6bd8b-23b6-47c7-a9a0-8dc56833ca18"
    client_secret = "7ab90651-f1c6-4756-a980-3813bf682198"
    token = check_token_age('token_info.txt', org_id, client_secret)
    lang_code = "en-US"

    print("Token: ", token)

    manual_update(server_name, suff, org_id, token, kbase_list, lang_code, limit=5)



