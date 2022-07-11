import requests
import html
from tkinter import *


#-----------Data---------
response = requests.get(url="https://opentdb.com/api.php?amount=10&type=boolean")
response.raise_for_status()
data = response.json()

data_dict = {}
for result in data["results"]:
    data_dict[result["question"]] = result["correct_answer"]

question_list = list(data_dict)

#------------Generate Questions-------------
index = 0
score = 0
answer = ""
game_over = False


def get_question():
    canvas.config(bg="white")
    if index <= len(question_list) - 1:
        question = question_list[index]
        globals()["answer"] = data_dict[question]
        question = html.unescape(question)
        canvas.itemconfig(question_text, text=question)
        # print(question)
        # print(answer)
    else:
        canvas.itemconfig(question_text, text=f"Results: {score}/{len(question_list)} correct!\nThanks for playing!")
        globals()["game_over"] = True


def check_true():
    if not game_over:
        if answer == "True":
            globals()["score"] += 1
            score_label.config(text=f"Score: {score}")
            canvas.config(bg="green")
        else:
            canvas.config(bg="red")
        globals()["index"] += 1
        window.after(250, func=get_question)


def check_false():
    if not game_over:
        if answer == "False":
            globals()["score"] += 1
            score_label.config(text=f"Score: {score}")
            canvas.config(bg="green")
        else:
            canvas.config(bg="red")
        globals()["index"] += 1
        window.after(250, func=get_question)


#-------- UI ----------
THEME_COLOR = "#375362"
window = Tk()
window.title("Quizzler")
window.config(padx=50, pady=50, bg=THEME_COLOR)

title_label = Label(text="QUIZZLER", bg=THEME_COLOR, fg="white", font=("Arial", 48, "bold"))
title_label.grid(column=0, row=0, pady=10, columnspan=2)

score_label = Label(text=f"Score: {score}", bg=THEME_COLOR, fg="white", font=("Arial", 24, "normal"))
score_label.grid(column=0, row=1, columnspan=2)

canvas = Canvas(width=400, height=400, bg="white")
question_text = canvas.create_text(200, 200, width=350, text="This is where the questions will go", font=("Arial", 24, "italic"))
canvas.grid(column=0, row=3, pady=50, columnspan=2)

TRUE_IMAGE = PhotoImage(file="images/true.png")
true_button = Button(image=TRUE_IMAGE, highlightthickness=0, command=check_true)
true_button.grid(column=0, row=4)

FALSE_IMAGE = PhotoImage(file="images/false.png")
false_button = Button(image=FALSE_IMAGE, highlightthickness=0, command=check_false)
false_button.grid(column=1, row=4)

get_question()

window.mainloop()