from HTTPRequest import HTTPRequest
from suffix_keys import url_suff as suff

import requests
import json
import categories
import documents
import kbase
import training
import search

if __name__ == "__main__":

    server_name = "https://api.genesysappliedresearch.com"
    org_id = "3ae6bd8b-23b6-47c7-a9a0-8dc56833ca18"
    client_secret = "7ab90651-f1c6-4756-a980-3813bf682198"
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcmdJZCI6IjNhZTZiZDhiLTIzYjYtNDdjNy1hOWEwLThkYzU2ODMzY2ExOCIsImV4cCI6MTU3MTUyNjUxMiwiaWF0IjoxNTcxNTIyOTEyfQ.HVelm58b8HA4yx1PASrO84g8wAiQRCWtv73gYz7WtOQ"

    #payload_info = {"name": "Sample KBase",
    #                "description": "Testing our preliminary kbase!",
     #               "coreLanguage": "en-US"}

    #kbase_responses = {}

    print("-----------------------------------------------------------")
    #kbase.create_kbase(server_name,suff,payload_info,org_id,token,kbase_responses)

    #VIEW Knowledge-Base
    print("-----------------------------------------------------------")
    resp_list = kbase.view_kbase(server_name, suff, org_id, token, limit=5, kbase_id=None)
    print(resp_list)
    #List: ['891c0775-18d5-4f4c-9222-314a7ff650ac', '254a5aae-225f-412c-98c2-b1f5dfd6c6b9', 'fd41a9b6-442c-44d5-b6b7-0317d6add350', '68e2b7b8-b3cd-4af0-b21b-f699ea9d3a00', '6bda054f-e54d-4232-96e5-34c59bf2b0f5']

    #Load 5 Docs
    # questions = ["What is the state dessert of Arizona?",
    # "What is the national spirit of America?",
    # "In 1963, which state sold the first fried dill pickle?",
    # "Name the state which is the birthplace of Cheeseburger?",
    # "What is the national dish of Germany?"]
    #
    # answers = ["Lane Cake","Bourbon","Arkansas","Colorado","Pot Roast"]
    #
    kbase1_id = '891c0775-18d5-4f4c-9222-314a7ff650ac'
    lang_code = "en-US"
    #
    print("-----------------------------------------------------------")
    # for i in range(1,5):
    #     payload = {"question":questions[i],"answer":answers[i]}
    #     documents.upload_doc(server_name, suff, kbase1_id, lang_code, payload, org_id, token, categories={})

    #TRAIN!
    print("-----------------------------------------------------------")
    #training_id = training.train_model(server_name, suff, kbase1_id, lang_code, org_id, token)
    #print("Training ID: ",training_id)

    #Check Training!
    print("-----------------------------------------------------------")
    training_id = "12143149-114c-40f5-8b09-6f7b7df88530"
    status_code = training.view_trained_model(server_name, suff, kbase1_id, lang_code,training_id, org_id, token)
    print("status code: ", status_code)

    #Try search query!
    print("-----------------------------------------------------------")
    payload = {"query":"What is the national spirit of Canada?"}
    results = search.search(server_name, suff, kbase1_id, payload, org_id, token)
    print(results)
    #print(kbase_responses)