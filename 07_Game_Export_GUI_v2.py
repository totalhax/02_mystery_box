from tkinter import *
from functools import partial
import random


class Game:
    def __init__(self):
        self.game_stats_list = [50, 6]
        self.round_stats_list = [' silver ($4)']

        self.game_frame = Frame()
        self.game_frame.grid()
        self.heading_label = Label(self.game_frame, text="Play...",
                                   font="Arial 24 bold", padx=10,
                                   pady=10)
        self.heading_label.grid(row=0)
        self.stats_button = Button(self.game_frame,
                                   text="Game Stats",
                                   font="Arial 14", padx=10, pady=10,
                                   command=lambda: self.to_stats(self.round_stats_list, self.game_stats_list)
                                   )

        self.stats_button.grid(row=1)

    def to_stats(self, game_history, game_stats):
        GameStats(self, game_history, game_stats)


class GameStats:
    def __init__(self, partner, game_history, game_stats):

        print(game_history)

        partner.stats_button.config(state=DISABLED)
        heading = "Arial 12 bold"
        content = "Atial 12"
        self.stats_box = Toplevel()
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))
        self.stats_frame = Frame(self.stats_box)
        self.stats_frame.grid()
        self.stats_heading_label = Label(self.stats_frame, text="Game Statistics",
                                         font="arial 19 bold")
        self.stats_heading_label.grid(row=0)
        self.export_instructions = Label(self.stats_frame,
                                         text="Here are your Game Statistics."
                                              "Please use the Export button to "
                                              "access to the results of each "
                                              "round that you played", wrap=250,
                                         font="arial 10 italic",
                                         justify=LEFT, fg="green",
                                         padx=10, pady=10)

        # instructions (row 1)
        self.export_instructions.grid(row=1)

        # Strating balance (row 2)
        self.details_frame = Frame(self.stats_frame)
        self.details_frame.grid(row=2)


        self.start_balance_label = Label(self.details_frame,
                                        text="Starting Balance:", font=heading,
                                        anchor="e")
        self.start_balance_label.grid(row=0, column=0, padx=0)
        self.start_balance_value_label = Label(self.details_frame, font=content,
                                               text="${}".format(game_stats[0]), anchor="e")
        self.start_balance_value_label.grid(row=0, column=1, padx=0)
        self.current_balance_label = Label(self.details_frame,
                                           text="Current Balance:", font=heading,
                                           anchor="w")
        self.current_balance_label.grid(row=1, column=0, padx=0)
        self.current_balance_value_label = Label(self.details_frame, font=content,
                                                 text="${}".format(game_stats[1]), anchor="w")
        self.current_balance_value_label.grid(row=1, column=1, padx=0)
        if game_stats[1] > game_stats[0]:
            win_loss = "Amount Won:"
            amount = game_stats[1] - game_stats[0]
            win_loss_fg = "green"
        else:
            win_loss = "Amount Lost:"
            amount = game_stats[0] - game_stats[1]
            win_loss_fg = '#660000'

        self.wind_loss_label = Label(self.details_frame,
                                     text=win_loss, font=heading,
                                     anchor="e")
        self.wind_loss_label.grid(row=2, column=0, padx=0)
        self.wind_loss_value_label = Label(self.details_frame, font=content,
                                           text="${}".format(amount),
                                           fg=win_loss_fg, anchor="w")
        self.wind_loss_value_label.grid(row=2, column=1, padx=0)
        self.games_played_label = Label(self.details_frame,
                                       text="Round Played:", font=heading,
                                       anchor="e")
        self.games_played_label.grid(row=4, column=0, padx=0)
        self.games_played_value_label = Label(self.details_frame, font=content,
                                              text=len(game_history),
                                              anchor="w")
        self.games_played_value_label.grid(row=4, column=1, padx=0)

        # Buttons, row 3 of stats frame
        self.export_quit_frame = Frame(self.stats_frame)
        self.export_quit_frame.grid(row=3)

        self.dismiss_btn = Button(self.export_quit_frame, text="Dismiss",
                                  command=partial(self.close_stats, partner))
        self.dismiss_btn.grid(row=0, column=0)

        self.export_btn = Button(self.export_quit_frame, text="Export",
                                 command=lambda: self.export(game_history, all_game_stats))
        self.export_btn.grid(row=0, column=1)

    def close_stats(self, partner):
        # Put help button back to normal
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()

    def export(self, game_history, all_game_stats):
        Export(self, game_history, all_game_stats)


class Export:
    def __init__(self, partner, game_history, all_game_stats):
        print(game_history)
        partner.export_btn.config(state=DISABLED)
        self.export_box = Toplevel()
        self.export_box.protocol('WM_DELETE_WINDOW', partial(self.close_export, partner))
        self.export_frame = Frame(self.export_box, width=300)
        self.export_frame.grid()
        self.how_heading = Label(self.export_frame, text="Export / "
                                                         "Instructions",
                                 font="arial 14 bold")
        self.how_heading.grid(row=0)
        self.export_text = Label(self.export_frame, text="Enter a filename in the "
                                                         "box below and press the "
                                                         "Save button to save your "
                                                         "calculation history to a "
                                                         "text file.")
        self.export_text.grid(row=1)
        self.export_text = Label(self.export_frame, text="If the filename you "
                                                         "enter below already "
                                                         "exists, its contents "
                                                         "will be replaced with "
                                                         "your calculation history.",
                                 justify=LEFT, bg="#ffafaf", fg="maroon",
                                 font="Arial 10 italic", wrap=225, padx=10, pady=10)
        self.export_text.grid(row=2, pady=10)
        self.filename_entry = Entry(self.export_frame, width=20,
                                    font="Arial 14 bold", justiy=CENTER)
        self.filename_entry.grid(row=3, pady=10)
        self.save_error_label = Label(self.export_frame, text="", fg="maroon")
        self.save_error_label.grid(row=4)
        self.save_cancel_frame = Frame(self.export_frame)
        self.save_cancel_frame.grid(row=5, pady=10)
        self.save_button = Button(self.save_cancel_frame, text="Save",
                                  font="Arial 15 bold", bg="#003366", fg="white",
                                  command=partial(lambda: self.save_history(partner, game_history, all_game_stats)))
        self.save_button.grid(row=0, column=1)
        self.cancel_button = Button(self.save_cancel_frame, text="Cancel",
                                    font=" Arial 15 bold", bg="#660000", fg="white",
                                    command=partial(self.close_export, partner))
        self.cancel_button.grid(row=0, column=1)

        def close_export(self, partner):
            # Put help button back to normal
            partner.export_button.config(state=NORMAL)
            self.stats_box.destroy()

    def save_history(self, partner, game_history, game_stats):
        valid_char = "[A-Za-z0-9_]"
        has_error = "no"
        filename = self.filename_entry.get()
        print(filename)
        for letter in filename:
            if re.match(valid_char, letter):
                continue
            elif letter == " ":
                problem = "(no spaces allowed)"
            else:
                problem = ("(no {}'s allowed)".format(letter))
            has_error = "yes"
            break
        if filename == "":
            problem = "can't be blank"
            has_error = "yes"
        if has_error == "yes":
            self.save_error_label.config(text="Invalid filename - {}".format(problem))
            self.filename_entry.config(bg="#ffafaf")
            print()
        else:
            filename = filename + ".txt"
            f = open(filename, "w+")
            f.write("Game Statistics\n\n")
            for round in game_stats:
                f.write(round + "\n")
            f.write("\nRound Details/n/n")
            for item in game_history:
                f.write(item + "\n")

            f.close()




# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box")
    something = Game()
    root.mainloop()
