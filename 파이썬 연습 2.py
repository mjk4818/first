from tkinter import *
import tkinter as tk
import customtkinter
import random


users = {"nix4828": "thsths4828"}

def check_data():
    username = user_id.get()
    password_input = password.get()

    if username in users and users[username] == password_input:
        window.destroy()
        start_game()
    else:
        print("Check your Username/Password")

def start_game():
    newwin = Tk()
    newwin.title("Tick Tack Toe")

    players = ["X", "O"]
    player = random.choice(players)
    buttons = [[None, None, None],
               [None, None, None],
               [None, None, None]]

    def next_turn(row, column):
        nonlocal player

        if buttons[row][column].get() == "" and check_winner() is False:
            buttons[row][column].set(player)

            if check_winner() is False:
                player = players[1] if player == players[0] else players[0]
                label.config(text=(player + " turn"))

            elif check_winner() is True:
                label.config(text=(players[0] + " wins"))

            elif check_winner() == "Tie":
                label.config(text=("Tie!"))

    def check_winner():
        for row in range(3):
            if buttons[row][0].get() == buttons[row][1].get() == buttons[row][2].get() != "":
                return True

        for column in range(3):
            if buttons[0][column].get() == buttons[1][column].get() == buttons[2][column].get() != "":
                return True

        if buttons[0][0].get() == buttons[1][1].get() == buttons[2][2].get() != "":
            return True

        elif buttons[0][2].get() == buttons[1][1].get() == buttons[2][0].get() != "":
            return True

        elif not empty_spaces():
            return "Tie"

        else:
            return False

    def empty_spaces():
        spaces = 9
        for row in range(3):
            for column in range(3):
                if buttons[row][column].get() != "":
                    spaces -= 1
        if spaces == 0:
            return False
        else:
            return True

    def new_game():
        nonlocal player

        player = random.choice(players)
        label.config(text=player + " turn")

        for row in range(3):
            for column in range(3):
                buttons[row][column].set("")

    label = Label(newwin, text=player + " turn", font=('consolas', 40))
    label.pack(side="top")

    reset_button = customtkinter.CTkButton(newwin, text="Restart", font=('consolas', 20), command=new_game)
    reset_button.pack(side="top")

    frame = Frame(newwin)
    frame.pack()

    for row in range(3):
        for column in range(3):
            buttons[row][column] = StringVar()
            button = Button(frame, text="", relief="groove", borderwidth="5", font=('consolas', 40),width='5', height='2', textvariable=buttons[row][column],
                            command=lambda row=row, column=column: next_turn(row, column))
            button.grid(row=row, column=column)

    newwin.mainloop()

def register():
    def save_data():
        new_user = new_user_id.get()
        new_pass = new_password.get()

        if new_user not in users:
            users[new_user] = new_pass
            print("Registration Successful")
            newwin.destroy()
        else:
            print("Username already exists")

    newwin = Tk()
    newwin.title("Register")

    new_user_id, new_password = StringVar(), StringVar()

    tk.Label(newwin, text="New Username : ").pack()
    tk.Label(newwin, text="New Password : ").pack()
    tk.Entry(newwin, textvariable=new_user_id).pack()
    tk.Entry(newwin, textvariable=new_password, show='*').pack()
    tk.Button(newwin, text="Register", command=save_data).pack()

window = Tk()
window.title("Login")

user_id, password = StringVar(), StringVar()

tk.Label(window, text="Username : ").grid(row=0, column=0, padx=10, pady=10)
tk.Label(window, text="Password : ").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(window, textvariable=user_id).grid(row=0, column=1, padx=10, pady=10)
tk.Entry(window, textvariable=password, show='*').grid(row=1, column=1, padx=10, pady=10)
customtkinter.CTkButton(window, text="Login", command=check_data).grid(row=2, column=1, padx=10, pady=10)

register_button = customtkinter.CTkButton(window,text="Register", command=register)
register_button.grid(row=3, column=1, padx=10, pady=10)

window.mainloop()
