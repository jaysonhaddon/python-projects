import turtle
import pandas

saved_data = pandas.read_csv("50_states_save_data.csv")
states_data = pandas.read_csv("50_states.csv")
states_list = states_data["state"].to_list()
num_states = len(states_list)
num_correct = 0

save_list = saved_data["state"].to_list()
save_dict = {
    "state" : save_list
}

screen = turtle.Screen()
screen.title("Python States Game")
screen.setup(width=725, height=491)
screen.bgpic("blank_states_img.gif")


def get_state_position(state):
    state_row = states_data[states_data["state"] == state]
    xpos = int(state_row["x"])
    ypos = int(state_row["y"])
    create_state_icon(state, xpos, ypos)


def create_state_icon(state_name, state_xpos, state_ypos):
    state = turtle.Turtle()
    state.hideturtle()
    state.penup()
    state.speed("fastest")
    state.goto(state_xpos, state_ypos)
    state.write(state_name, align="center", font=("Arial", 8, "normal"))


def save_game():
    save_file = pandas.DataFrame(save_dict)
    save_file.to_csv("50_states_save_data.csv")


user_input = screen.textinput("Load Game", "Would you like to load a game? Type 'yes' or 'no':").lower()
if user_input == "yes":
    for state in save_list:
            get_state_position(state)
            num_correct += 1
else:
    save_list.clear()
    save_game()
    

while num_correct < num_states:
    user_input = screen.textinput(f"{num_correct}/{num_states} States Correct", "Guess a state name: ").title()
    if user_input in states_list:
        get_state_position(user_input)
        save_list.append(user_input)
        save_game()
        num_correct += 1


screen.exitonclick()

