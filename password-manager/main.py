from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json



# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def random_selection(char_amount, char_list, pass_list):
    for _ in range(0, char_amount):
        random_choice = random.choice(char_list)
        pass_list.append(random_choice)


def random_capital_letters(pass_list):
    for num in range(len(pass_list)):
        random_num = random.randint(1, 10)
        if random_num % 2 == 0:
            pass_list[num] =  pass_list[num].upper()


def create_shuffled_password(pass_list):
    for _ in range(3):
        random.shuffle(pass_list)
    password = "".join(pass_list)  
    return password


def generate_password():
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    special = ["!", "@", "#", "$", "%", "^", "&", "*"]
    password_list = []

    num_letters = random.randint(8,10)
    num_numbers = random.randint(2,4)
    num_special = random.randint(2,4)

    random_selection(num_letters, letters, password_list)
    random_capital_letters(password_list)
    random_selection(num_numbers, numbers, password_list)
    random_selection(num_special, special, password_list)
    new_password = create_shuffled_password(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, new_password)
    pyperclip.copy(new_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    name = name_entry.get().title()
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {
        name: {
            "website": website,
            "username": username,
            "password": password,
        }       
    }

    if len(name) == 0 or len(website) == 0 or len(password) == 0 or len(username) == 0:
        messagebox.showwarning(title="Missing Information", message="Please complete all of the required fields")
    else:
        confirm_message = f"Website: {website}\nEmail/Username: {username}\nPassword: {password}\nSave {name} entry?"
        user_validation = messagebox.askokcancel(title=f"Create {name} Entry", message=confirm_message)
        
        if user_validation:
            try:
                with open("./data.json", "r") as save_file:
                    save_data = json.load(save_file)
                    save_data.update(new_data)
            except FileNotFoundError:
                with open("./data.json", "w") as save_file:
                    json.dump(new_data, save_file, indent=4)
            else:
                with open("./data.json", "w") as save_file:
                    json.dump(save_data, save_file, indent=4)
            name_entry.delete(0, END)
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# -------------------------- SEARCH DATA ------------------------------ #
def search():
    name_key = name_entry.get().title()
    try:
        with open("./data.json", "r") as save_file:
            save_data = json.load(save_file)
        save_value = save_data[name_key]
    except FileNotFoundError:
        messagebox.showwarning(title="Missing File", message="No Save Data file found")
    except KeyError:
        messagebox.showwarning(title="Invalid Name", message="That Name does not exist in the Save Data")
    else:
        name_entry.delete(0, END)
        website_entry.delete(0, END)
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        name_entry.insert(0, name_key)
        website_entry.insert(0, save_value["website"])
        username_entry.insert(0, save_value["username"])
        password_entry.insert(0, save_value["password"])
        messagebox.showinfo(title=f"{name_key}", message=f"Website: {website_entry.get()}\nUsername: {username_entry.get()}\nPassword: {password_entry.get()}")



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

logo_canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
logo_canvas.create_image(100, 100, image=logo_image)
logo_canvas.grid(column=1, row=0)

name_label = Label(text="Name:")
name_label.grid(column=0, row=1)

website_label = Label(text="Website:")
website_label.grid(column=0, row=2)

username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=3)

password_label = Label(text="Password:")
password_label.grid(column=0, row=4)

name_entry = Entry()
name_entry.grid(column=1, row=1, sticky="EW")
name_entry.focus()

name_button = Button(text="Search", command=search)
name_button.grid(column=2, row=1, sticky="EW")

website_entry = Entry()
website_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
website_entry.focus()

username_entry = Entry()
username_entry.grid(column=1, row=3, columnspan=2, sticky="EW")

password_entry = Entry()
password_entry.grid(column=1, row=4, sticky="EW")

password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(column=2, row=4, sticky="EW")

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=5, columnspan=2, sticky="EW")


window.mainloop()