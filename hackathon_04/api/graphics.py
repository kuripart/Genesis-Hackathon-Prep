import tkinter as tk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import user_platform

def create_radio_button(window,x,y,diff_v,text_list):
    v = IntVar()
    rad_list = []
    for i in range(len(text_list)):
        rad_list.append(Radiobutton(window, text=text_list[i], variable=v, value=i+1).place(relx=x, rely=y+i*diff_v, anchor="nw"))
    return rad_list

def process_user_question(window, q_entry, num_answers_rad_list, chart_type_rad_list, data_type_rad_list):
    create_list_box(window, q_entry.get())
    #q_entry.delete(0, END)
    make_pie_chart(window)


def create_window(title_in):
    window = tk.Tk()
    window.geometry("700x500")
    window.title(title_in)
    return window

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

def create_list_box(window, q_text):
    Lb = Listbox(window)
    Lb.insert(1, q_text)
    Lb.place(relx=0.2, rely=0.75, anchor=CENTER)
    return Lb

#
# How to Create a GUI in Python
def make_pie_chart(window):
    # USED: https://datatofish.com/how-to-create-a-gui-in-python/

    canvas1 = tk.Canvas(window, width=325, height=450, bg='#ffffff')  # create the canvas (tkinter module)
    canvas1.place(relx=0.45, rely=0.01)

    def insert_number(x1, x2, x3):  # create a function/command to be called by the button (i.e., button2 below)
        pass

        # create a bar chart once the variables x1, x2 and x3 are inserted
        # by the user (and the user then clicks on button2 below)
        # figure1 = Figure(figsize=(5,4), dpi=100) # create a Figure (matplotlib module)
        # subplot1 = figure1.add_subplot(111) # add a subplot
        # intakes the values inserted under x1, x2 and x3 to represent the x Axis
        # xAxis = [float(x1),float(x2),float(x3)]
        # intakes the values inserted under x1, x2 and x3 to represent the y Axis
        # yAxis = [float(x1),float(x2),float(x3)]
        # subplot1.bar(xAxis,yAxis, color = 'g') # create the bar chart based on the input variables x1, x2, and x3
        # bar1 = FigureCanvasTkAgg(figure1, window) # create a canvas figure (matplotlib module)
        # bar1.get_tk_widget().place(relx=0.5, rely=0.2, anchor=CENTER)
        # create a pie chart once the variables x1, x2 and x3
        # are inserted by the user (and the user then clicks on button2 below)

        figure2 = Figure(figsize=(5, 4), dpi=50)  # create a Figure (matplotlib module)
        subplot2 = figure2.add_subplot(111)  # add a subplot
        labels2 = 'Label1', 'Label2', 'Label3'  # add labels for each slice in the pie chart
        pieSizes = [float(x1), float(x2),
                    float(x3)]  # intakes the values inserted under x1, x2 and x3 to represent the pie slices
        # explode2 = (0, 0.1, 0)  # explodes the 2nd slice (i.e. 'Label2')
        subplot2.pie(pieSizes, labels=labels2, autopct='%1.1f%%', shadow=True,
                     startangle=90)  # create the pie chart based on the input variables x1, x2, and x3
        subplot2.axis('equal')  # Use equal to draw the pie chart as a circle
        pie2 = FigureCanvasTkAgg(figure2, window)  # create a canvas figure (matplotlib module)
        pie2.get_tk_widget().place(relx=0.5, rely=0.3)

    insert_number(0.1, 0.2, 0.7)

if __name__ == '__main__':
    window = create_window('KNOWLEDGE BASE UI')
    create_label(window, 'Ask your question...', 0.1, 0.05)
    create_label(window, 'How \n Many \n Answers?', 0.05, 0.3)
    q_entry = create_entry(window, 0.025, 0.1, 50, 20)
    # lim_entry = create_entry(window, 0.2, 0.4, 10, 5)
    # canvas = create_canvas(window)
    # list_box = create_list_box(window, entry)
    num_answers_rad_list = create_radio_button(window,0.1,0.175,0.05,[1,2,3,4,5])
    chart_type_rad_list = create_radio_button(window, 0.2, 0.2, 0.05, ["bar", "pi"])
    data_filter_rad_list = create_radio_button(window, 0.3, 0.2, 0.05, ["normalized", "raw"])
    create_button(window, '#fff000', '#ff0000', '#f0b40e', 10, 10, 1, "Go!", 0.2, 0.5,
                  command=lambda: process_user_question(window, q_entry, num_answers_rad_list, chart_type_rad_list, data_filter_rad_list))

    window.mainloop()



