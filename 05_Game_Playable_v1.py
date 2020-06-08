from tkinter import *
import random

class Start:
    def __init__(self, parent):
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.push_me_button = Button(text="Push Me", command=self.to_game)
        self.push_me_button.grid(row=0, pady=10)

    def to_game(self):
        starting_balance = 50
        stakes = 2

        Game(self, stakes, starting_balance)

        root.withdraw()

class Game:
    def __init__(self, partner, stakes, starting_balance):
        print(stakes)