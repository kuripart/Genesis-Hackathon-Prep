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
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from matplotlib.figure import Figure
import os

kbase_list = []

def integrate_stats_with_ui(server_name, suff, org_id, token, kbase_list, lang_code, query='', search_size=5):
    return search_trained_kbase(server_name, suff, org_id, token, kbase_list, lang_code, query=query, search_size=search_size)

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

    with open(fname, "r") as file:
        file_size = len(file.readlines())
        while file_size-curr >= batch_size:
            batch_start_indices.append(curr)
            curr += batch_size
            batch_size_list.append(batch_size)
        if curr % batch_size != 0:
            batch_start_indices.append(curr)
            batch_size_list.append(file_size-curr)

    return (batch_size_list, batch_start_indices)


def upload_knowledge_batch(q_fname, a_fname, line_start_index, num_items, server_name, suff, kbase_id1, lang_code, org_id,token):
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
        payload = {
            "question": question,
            "answer": answer
        }
        documents.upload_doc(server_name, suff, kbase_id1, lang_code, payload, org_id, token, categories={})
        count += 1
        if count >= line_end_index:
            print("BREAKING! Count: ", count, "||| Line_End_Index: ", line_end_index)
            break
    print("NUM UPLOADS:", count-line_start_index)

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



def search_trained_kbase(server_name, suff, org_id, token, kbase_list, lang_code, query, search_size=5):
    print("---------------------VIEWING KBASES----------------------")

    #Process query


    kbase_ids = view_kbases(server_name, suff, org_id, token, limit=2)

    freq_words_list = ["freq_words_geography.txt","freq_words_history.txt"]
    kbase_id_sel = document_distance_simple(query, kbase_ids, freq_words_list).strip()

    print("---------------------SEARCH TRAINED KBASE AND GET THE TOP 5 ANSWERS-------------------")
    results_list = []
    confidence_list = []
    payload = {"query": query}
    print("QUERY: ", query)
    print("KBASE ID SEL: ", kbase_id_sel)
    results = search.search(server_name, suff, kbase_id_sel, payload, org_id, token, search_size=search_size)

    for result in results:
        results_list.append(result["faq"]["answer"])
        confidence_list.append(result["confidence"])
    print(results_list)
    print(confidence_list)
    return (results_list, confidence_list)

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

############################# GRAPHICS FUNCTIONS #########################################

def process_user_question(window, q_entry, num_answers_radio_var, chart_type_radio_var, data_type_radio_var,
                          server_name, suff, org_id, token, kbase_list, lang_code):

    lim_entry = int(num_answers_radio_var.get())
    chart_type = int(chart_type_radio_var.get()) #1 for bar, 2 for pi
    data_type = int(data_type_radio_var.get()) #1 for raw, 2 for normalized

    if q_entry.get():
        list_of_responses_per_training, list_of_respec_confidence = integrate_stats_with_ui(server_name, suff,
                                                                                        org_id, token,
                                                                                        kbase_list, lang_code,
                                                                                        query=q_entry.get(),
                                                                                        search_size=lim_entry)

        create_list_box(window, list_of_responses_per_training, kbase_list)
        #q_entry.delete(0, END)
        print('conf list: ', list_of_respec_confidence)
        make_chart(window, list_of_respec_confidence, chart_type, data_type)
    else:
        messagebox.showinfo("WARNING", "Please enter a query to use this application!")

def create_window(title_in):
    window = tk.Tk()
    window.geometry("900x550")  # 700 by 500
    window.title(title_in)
    return window

def create_radio_button(window,x,y,diff_v,text_list):
    radio_var = IntVar()
    rad_list = []
    for i in range(len(text_list)):
        rad_list.append(Radiobutton(window, text=text_list[i], variable=radio_var, value=i+1).place(relx=x, rely=y+i*diff_v, anchor="nw"))
    radio_var.set(1)
    return radio_var

def create_button(window, activebackground=None, activeforeground=None, bg=None,
                  font=None, width=None, height=None, text=None, x=None, y=None, command=None):
    button = tk.Button(window, activebackground=activebackground,
                       activeforeground=activeforeground,
                       bg=bg,
                       command=command,
                       font=font,
                       width=width,
                       height=height,
                       text=text)
    # button.bind("<Button-1>", test, del_text(entry))
    button.place(relx=x, rely=y, anchor=CENTER)


def create_label(window, text, x, y):
    label = Label(window, text=text).place(relx=x, rely=y, anchor=CENTER)
    return label


def create_entry(window, x, y, width, height):
    e1 = Entry(window,width=str(width))
    e1.place(relx=x, rely=y, anchor="nw")
    return e1

def create_canvas(window):
    can1 = Canvas(window, width=100, height=100, bg='#ffffff')
    can1.place(relx=0.2, rely=0.6, anchor=CENTER)
    return can1

def fill_canvas(canvas, entry):
    # canvas.create_text(100, 10, fill="darkblue", font="Times 20 italic bold", text=text)
    pass

def create_list_box(window, responses, kbase_id):
    Lb = Listbox(window)
    Lb.place(relx=0.2, rely=0.75, width = 350, anchor=CENTER)

    if len(responses) == 0:
        Lb.insert(0,"NO DATA FOUND ON QUERY!")
        return Lb

    kbase_ids = ['02a88583-3d53-4e6f-bbee-addb3d402d46', '978779fc-3c85-4d4a-927f-460b086f34a8']

    if kbase_id == kbase_ids[0]:
        Lb.insert(0,"KBASE BEING SEARCHED: Geography")
    else:
        Lb.insert(0,"KBASE BEING SEARCHED: History")

    for i in range(len(responses)):
        Lb.insert(i+1, "[" + str(i+1) + "] " + responses[i])

    return Lb

# How to Create a GUI in Python: CREDIT: https://datatofish.com/how-to-create-a-gui-in-python/
def make_chart(window, list_of_respec_confidence, chart_type, data_type):
    canvas1 = tk.Canvas(window, width=425, height=500, bg='#ffffff')  # create the canvas (tkinter module)
    canvas1.place(relx=0.45, rely=0.01)

    def insert_number(args, chart_type, data_type):  # create a function/command to be called by the button (i.e., button2 below)
        old_args = args[:]
        print("Args Length: ", len(args))
        print("Args: ", args)

        if data_type == 2:
            new_args = []
            arg_sum = sum(args)
            for arg in args:
                new_args.append(arg / arg_sum)
            args = new_args

        font = {'size': 12}
        matplotlib.rc('font', **font)

        if chart_type == 1:
            #PIE CHART
            figure2 = Figure(figsize=(5, 6), dpi=60)  # create a Figure (matplotlib module)
            subplot2 = figure2.add_subplot(111)  # add a subplot

            labels2 = []
            for i in range(len(args)):
                labels2.append("["+str(i+1)+"]")

            pieSizes = args  # intakes the values inserted under x1, x2 and x3 to represent the pie slices
            # explode2 = (0, 0.1, 0)  # explodes the 2nd slice (i.e. 'Label2')
            subplot2.pie(pieSizes, labels=labels2, autopct='%1.1f%%', shadow=True,
                         startangle=90)  # create the pie chart based on the input variables x1, x2, and x3
            subplot2.axis('equal')  # Use equal to draw the pie chart as a circle
            pie2 = FigureCanvasTkAgg(figure2, window)  # create a canvas figure (matplotlib module)
            pie2.get_tk_widget().place(relx=0.5, rely=0.2,anchor='nw')

        else:
            # BAR CHART
            figure1 = Figure(figsize=(5,6), dpi=60) # create a Figure (matplotlib module)
            subplot1 = figure1.add_subplot(111) # add a subplot
            yAxis = args
            xAxis = []
            for i in range(len(args)):
                xAxis.append(i+1)
            our_colours = list('rgbkymc')


            plt = subplot1.bar(xAxis,yAxis) # create the bar chart based on the input variables x1, x2, and x3
            for i in range(len(args)):
                plt[i].set_color(our_colours[i])

            bar1 = FigureCanvasTkAgg(figure1, window) # create a canvas figure (matplotlib module)
            bar1.get_tk_widget().place(relx=0.5, rely=0.2,anchor='nw')

    insert_number(list_of_respec_confidence, chart_type, data_type)  # TEST

def process_word_count(string_in, filename_rem_words):

    word_dict = {}

    punctuations = [",", ".", "!", ";", ":", "?", "/", "\\"]
    # punctuations = ['?','!']


    line_list = string_in.split(" ")

    for word in line_list:
        word = word.strip().lower()
        # print("word: ", word)

        # Remove punctuations
        list_word = list(word)
        # print("list_word: ", list_word)
        new_list_word = []
        # print("new list word (init): ", new_list_word)
        for char in list_word:
            # print("Examining char: ", char)
            # print("Equality: ", char in punctuations)
            if char not in punctuations:
                # print("in IF!")
                new_list_word.append(char)
            # print("New list word: ", new_list_word)
        new_word = "".join(new_list_word)

        if new_word in word_dict.keys():
            word_dict[new_word] += 1
        else:
            word_dict[new_word] = 1
# print("DICT WORDS: ", word_dict)

    print(word_dict)

    # REMOVE the trivial words (eg. or, as , with, etc)
    with open(filename_rem_words, 'r') as file:
        rem_words = file.readlines()
        # print("Word dict keys: ", word_dict.keys())
        # print("Rem words: ", rem_words)
        for i in range(len(rem_words)):
            rem_words[i] = rem_words[i].strip()
            word = rem_words[i]

            if word in word_dict.keys():
                # print("Removing: ",word)
                word_dict.pop(word)

    key_issue = None
    for key in word_dict.keys():
        if len(key) == 0:
            key_issue = key
        # print("Key: ",key,"Length: ",len(key))
    if key_issue != None:
        word_dict.pop(key_issue)

    return word_dict

def document_distance_simple(input_string, kbase_id_list, freq_words_list):

    checker_filename = "stopwords.txt"

    string_word_dict = process_word_count(input_string,checker_filename)

    print("String word dict: ", string_word_dict)
    hit_rate_vec = []
    max_index = 0
    max_hit_rate = 0

    for i in range(len(kbase_id_list)):

        hit_rate = 0
        #Read frequency file!git ad
        with open(freq_words_list[i], 'r') as file:
            print("---------------------------------")
            lines = file.readlines()
            # print("Lines: ", lines)
            for line in lines:
                line = line.strip()
                line = line.split(",")
                key, val = line[0], int(line[1])

                if key in string_word_dict:
                    print("key: ", key," string_word_dict[key]", string_word_dict[key],"doc_dict[key]: ",val)
                    hit_rate += min(string_word_dict[key],val)
        hit_rate_vec.append(hit_rate)
        if hit_rate > max_hit_rate:
            max_hit_rate = hit_rate
        max_index += 1

    print(hit_rate_vec)
    print(kbase_id_list)

    kbase_to_search = kbase_id_list[max(0,max_index-1)]

    return kbase_to_search
    # freq_words_list = ["freq_words_geography.txt","freq_words_history.txt"]
    # kbase_list = view_kbases(server_name, suff, org_id, token, limit=limit)
    # print(document_distance_simple("islas gulf lake honolulu hudson", kbase_list, freq_words_list))

if __name__ == '__main__':
    server_name = "https://api.genesysappliedresearch.com"
    org_id = "3ae6bd8b-23b6-47c7-a9a0-8dc56833ca18"
    client_secret = "7ab90651-f1c6-4756-a980-3813bf682198"
    token = check_token_age('token_info.txt', org_id, client_secret)
    print("Token: ", token)
    lang_code = "en-US"
    limit = 5

    #GRAPHICS HANDLING
    window = create_window('KNOWLEDGE BASE UI')
    create_label(window, 'Ask your question...', 0.1, 0.05)
    create_label(window, 'How \n Many \n Answers?', 0.05, 0.3)
    q_entry = create_entry(window, 0.025, 0.1, 50, 20)
    # lim_entry = create_entry(window, 0.2, 0.4, 10, 5)
    # canvas = create_canvas(window)
    # list_box = create_list_box(window, entry)
    num_answers_radio_var = create_radio_button(window,0.1,0.175,0.05,[1,2,3,4,5])
    chart_type_radio_var = create_radio_button(window, 0.2, 0.2, 0.05, ["pi","bar"])
    data_type_radio_var = create_radio_button(window, 0.3, 0.2, 0.05, ["raw", "normalized"])
    create_button(window, '#fff000', '#ff0000', '#f0b40e', 10, 10, 1, "Go!", 0.2, 0.5,
                  command=lambda: process_user_question(window, q_entry, num_answers_radio_var, chart_type_radio_var,
                                                        data_type_radio_var, server_name, suff,
                                                         org_id, token, kbase_list,
                                                         lang_code))

    window.mainloop()






