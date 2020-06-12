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

        self.start_frame.destroy()


class Game:
    def __init__(self, partner, stakes, starting_balance):
        print(stakes)
        print(starting_balance)
        self.balance = IntVar()
        self.balance.set(starting_balance)
        self.multiplier = IntVar()
        self.multiplier.set(stakes)
        self.game_box = Toplevel()
        self.game_box.protocol('WM_DELETE_WINDOW', self.to_quit)
        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()
        self.heading_label = Label(self.game_frame, text="Play...",
                                   font="Arial 24 bold", padx=10,
                                   pady=10)
        self.heading_label.grid(row=0)
        self.instructions_label = Label(self.game_frame, wrap=300, justify=LEFT,
                                        text="Press <enter> or click the 'Open "
                                             "Boxes' button to reveal the "
                                             "contents of the mystery boxes.",
                                        font="Arial 10", padx=10, pady=10)
        self.instructions_label.grid(row=1)
        box_text = "Arial 16 bold"
        box_back = "#b9ea96"
        box_width = 5
        self.box_frame = Frame(self.game_frame)
        self.box_frame.grid(row=2, pady=10)
        self.prize1_label = Label(self.box_frame, text="?\n", font=box_text,
                                  bg=box_back, width=box_width, padx=10, pady=10)
        self.prize1_label.grid(row=0, column=0)
        self.prize2_label = Label(self.box_frame, text="?\n", font=box_text,
                                  bg=box_back, width=box_width, padx=10, pady=10)
        self.prize2_label.grid(row=0, column=1, padx=10)
        self.prize3_label = Label(self.box_frame, text="?\n", font=box_text,
                                  bg=box_back, width=box_width, padx=10, pady=10)
        self.prize3_label.grid(row=0, column=2)
        self.play_button = Button(self.game_frame, text="Open Boxes",
                                  bg="#FFFF33", font="Arial 15 bold", width=20,
                                  padx=10, pady=10, command=self.reveal_boxes)
        self.play_button.grid(row=3)
        start_text = "Game Cost: ${} \n "" \nHow much " \
                     "will you win?".format(stakes * 5)
        self.balance_label = Label(self.game_frame, font="Arial 12 bold", fg="green",
                                   text=start_text, wrap=300,
                                   justify=LEFT)
        self.balance_label.grid(row=4, pady=10)
        self.help_export_frame = Frame(self.game_frame)
        self.help_export_frame.grid(row=5, pady=10)
        self.help_button = Button(self.help_export_frame, text="Help / Rules",
                                  font="Arial 15 bold",
                                  bg="#808080", fg="white")
        self.help_button.grid(row=0, column=0, padx=2)
        self.stats_button = Button(self.help_export_frame, text="Game Stats...",
                                   font="Arial 15 bold",
                                   bg="#808080", fg="white")
        self.stats_button.grid(row=0, column=1, padx=2)
        self.quit_button = Button(self.game_frame, text="Quit", fg="white",
                                  bg="#660000", font="Arial 15 bold", width=20,
                                  command=self.to_quit, padx=10, pady=10)
        self.quit_button.grid(row=6, pady=10)

    def reveal_boxes(self):
        current_balance = self.balance.get()
        stakes_multiplier = self.multiplier.get()
        round_winnings = 0
        prizes = []
        backgrounds = []
        for item in range(0, 3):
            prize_num = random.randint(1,100)
            if 0 < prize_num <= 5:
                prize = "gold\n(${})".format(5 * stakes_multiplier)
                back_color = "#CEA935"
                round_winnings += 5 * stakes_multiplier
            elif 5 < prize_num <= 25:
                prize = "silver\n(${})".format(2 * stakes_multiplier)
                back_color = "#B7B7B5"
                round_winnings += 2 * stakes_multiplier
            elif 25 < prize_num <= 65:
                prize = "copper\n(${})".format(1 * stakes_multiplier)
                back_color = "#BC7F61"
                round_winnings += stakes_multiplier
            else:
                prize = "lead\n($0)"
                back_color = "#595E71"
            prizes.append(prize)
            backgrounds.append(back_color)
        self.prize1_label.config(text=prizes[0], bg=backgrounds[0])
        self.prize2_label.config(text=prizes[1], bg=backgrounds[1])
        self.prize3_label.config(text=prizes[2], bg=backgrounds[2])
        current_balance -= 5 * stakes_multiplier
        current_balance += round_winnings
        self.balance.set(current_balance)
        balance_statement = "Game Cost: ${}\nPayback: ${} \n" \
                            "Current Balance: ${}".format(5 * stakes_multiplier,
                                                          round_winnings,
                                                          current_balance)
        self.balance_label.configure(text=balance_statement)

    def to_quit(self):
        root.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box Game")
    something = Start(root)
    root.mainloop()


