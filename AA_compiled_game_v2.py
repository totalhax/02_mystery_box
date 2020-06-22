from tkinter import *
from functools import partial
import random


class Start:
    def __init__(self, parent):

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.starting_funds = IntVar()
        self.starting_funds.set(0)

        self.mystery_box_label = Label(self.start_frame, text="Mystery Box Game",
                                       font="Arial 19 bold")
        self.mystery_box_label.grid(row=0)

        self.mystery_box_instructions = Label(self.start_frame, text="Please enter a dollar amount\n"
                                                                     "(between $5 and $50) in the \n"
                                                                     "box below. Then choose the\n"
                                                                     "stakes. The higher the stakes\n"
                                                                     ", the more you can win!")
        self.mystery_box_instructions.grid(row=1)

        self.entry_error_frame = Frame(self.start_frame, width=200)
        self.entry_error_frame.grid(row=2)

        self.start_amount_entry = Entry(self.entry_error_frame,
                                        font="Arial  19 bold", width=10)
        self.start_amount_entry.grid(row=0, column=0)

        self.add_funds_button = Button(self.entry_error_frame,
                                       font="Arial 14 bold",
                                       text="Add Funds",
                                       command=self.check_funds)
        self.add_funds_button.grid(row=0, column=1)

        self.amount_error_label = Label(self.entry_error_frame, fg="maroon",
                                        text="", font="Arial 10 bold", wrap=275,
                                        justify=LEFT)
        self.amount_error_label.grid(row=1, columnspan=2, pady=5)

        self.stakes_frame = Frame(self.start_frame)
        self.stakes_frame.grid(row=4)

        button_font = "Arial 10 bold"

        self.low_stakes_button = Button(self.stakes_frame, text="Low ($5)", background="orange",
                                        font=button_font,
                                        command=lambda: self.to_game(1))
        self.low_stakes_button.grid(row=0, column=0, pady=10,)

        self.medium_stakes_button = Button(self.stakes_frame, text="Medium ($10)", background="yellow",
                                           font=button_font,
                                           command=lambda: self.to_game(2))
        self.medium_stakes_button.grid(row=0, column=1, padx=5, pady=10)

        self.high_stakes_button = Button(self.stakes_frame, text="High ($15)", background="green",
                                         font=button_font,
                                         command=lambda: self.to_game(3))
        self.high_stakes_button.grid(row=0, column=2, pady=10)

        self.low_stakes_button.config(state=DISABLED)
        self.medium_stakes_button.config(state=DISABLED)
        self.high_stakes_button.config(state=DISABLED)

    def check_funds(self):
        starting_balance = self.start_amount_entry.get()

        error_back = "#ffafaf"
        has_errors = "no"

        self.start_amount_entry.config(bg="white")
        self.amount_error_label.config(text="")

        self.low_stakes_button.config(state=DISABLED)
        self.medium_stakes_button.config(state=DISABLED)
        self.high_stakes_button.config(state=DISABLED)

        try:
            starting_balance = int(starting_balance)

            if starting_balance < 5:
                has_errors = "yes"
                error_feedback = "Sorry, the least you can play with is $5"
            elif starting_balance > 50:
                has_errors = "yes"
                error_feedback = "Too high! The most you can risk in this " \
                                 "game is $50"

            elif starting_balance >= 15:
                self.low_stakes_button.config(state=NORMAL)
                self.medium_stakes_button.config(state=NORMAL)
                self.high_stakes_button.config(state=NORMAL)
            elif starting_balance >= 10:
                self.low_stakes_button.config(state=NORMAL)
                self.medium_stakes_button.config(state=NORMAL)
            else:
                self.low_stakes_button.config(state=NORMAL)

        except ValueError:
            has_errors = "yes"
            error_feedback = "Please enter a dollar amount (no text / decimals)"

        if has_errors == "yes":
            self.start_amount_entry.config(bg=error_back)
            self.amount_error_label.config(text=error_feedback)

        else:
            self.starting_funds.set(starting_balance)

    def to_game(self, stakes):
        starting_balance = self.starting_funds.get()

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
        self.round_stats_list = []
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
        self.play_button.focus()
        self.play_button.bind('<Return>', lambda e: self.reveal_boxes())
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
                                  font="Arial 15 bold", command=self.help,
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
        stats_prizes = []
        for item in range(0, 3):
            prize_num = random.randint(1,100)
            if 0 < prize_num <= 5:
                prize = "gold\n(${})".format(5 * stakes_multiplier)
                prize_list = "gold\n(${})".format(5 * stakes_multiplier)
                back_color = "#CEA935"
                round_winnings += 5 * stakes_multiplier
            elif 5 < prize_num <= 25:
                prize = "silver\n(${})".format(2 * stakes_multiplier)
                prize_list = "silver\n(${})".format(2 * stakes_multiplier)
                back_color = "#B7B7B5"
                round_winnings += 2 * stakes_multiplier
            elif 25 < prize_num <= 65:
                prize = "copper\n(${})".format(1 * stakes_multiplier)
                prize_list = "copper\n(${})".format(1 * stakes_multiplier)
                back_color = "#BC7F61"
                round_winnings += stakes_multiplier
            else:
                prize = "lead\n($0)"
                prize_list = "lead\n($0)"
                back_color = "#595E71"
            prizes.append(prize)
            stats_prizes.append(prize_list)
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

        round_summary = "{} | {} | {} - Cost: ${} | " \
                        "Payback: ${} | Current Balance: " \
                        "${}".format(stats_prizes[0], stats_prizes[1],
                                     stats_prizes[2],
                                     5 * stakes_multiplier, round_winnings,
                                     current_balance)
        self.round_stats_list.append(round_summary)
        print(self.round_stats_list)

        if current_balance < 5 * stakes_multiplier:
            self.play_button.config(state=DISABLED)
            self.game_box.focus()
            self.play_button.config(text="Game Over")

            balance_statement = "Current Balance: ${}\n" \
                                "Your balance is too low. You can only quit " \
                                "or view your stats. Sorry about that.".format(current_balance)
            self.balance_label.config(fg="#660000", font="Arial 10 bold",

                                      text=balance_statement)

    def to_quit(self):
        root.destroy()

    def help(self):
        Help(self)

class Help:
    def __init__(self, partner):
        background = "#b9ea96"

        # disable help button
        partner.help_button.config(state=DISABLED)

        # Sets up Child Window (ie: help box)
        self.help_box = Toplevel()

        # If users press cross at top, closes help and 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        # Set up GUI Frame
        self.help_frame = Frame(self.help_box, bg=background)
        self.help_frame.grid()

        # Set up Help heading (row 0)
        self.how_heading = Label(self.help_frame, text="Help / Instructions",
                                 font=("Arial", "15", "bold"), bg=background)
        self.how_heading.grid(row=0)
        # Help text (label, row 1)
        self.help_text = Label(self.help_frame, text="",
                               justify=LEFT, width=40, bg=background, wrap=250)
        self.help_text.grid(row=1)
        # Dismiss button (row 2)
        self.dismiss_btn = Button(self.help_frame, text="Dismiss",
                                  width=10, bg="red", font=("Arial", "12"),
                                  command=partial(self.close_help, partner))
        self.dismiss_btn.grid(row=2, pady=10)

        self.help_text.configure(text="Choose an amount to play with and then choose the stakes. "
                                      "Higher stakes cost more per round but you can win more as "
                                      "well. \n\n"
                                      "When you enter the play area, you will see three mystery "
                                      "boxes. To reveal the contents of the boxes, click the "
                                      "'Open Boxes' button. If you don't have enough money to play, "
                                      "the button will turn red and you will need to quit the  "
                                      "game. \n\n"
                                      "The contents of the boxes will be added to your balance. "
                                      "The boxes could contain... \n\n"
                                      "Low: Lead ($0) | Copper ($1) | Silver ($2) | Gold ($10)\n"
                                      "Medium: Lead ($0) | Copper ($2) | Silver ($4) | Gold ($25)\n"
                                      "High: Lead ($0) | Copper ($5) | Silver ($10) | Gold ($50)\n\n"
                                      "If each box contains gold, you earn $30 (low stakes). If "
                                      "they contain copper, silver and gold, you would receive "
                                      "$13 ($1 + $2 + $10) and so on.", font=("Arial", "8"))

    def close_help(self, partner):
        # Put help button back to normal
        partner.help_button.config(state=NORMAL)
        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box")
    something = Start(root)
    root.mainloop()
