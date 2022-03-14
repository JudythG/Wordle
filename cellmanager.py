from tkinter import Label, Canvas
import config
import tkinter

NUM_GUESSES = 6
WORD_LENGTH = 5
TURTLE_SIZE = 20
CELL_STRETCH = 2
CELL_SIZE = TURTLE_SIZE * CELL_STRETCH
CELL_DELTA = CELL_SIZE + 10  # amount of space to put between (including) cells
X_START = -CELL_DELTA * WORD_LENGTH / 2
Y_START = CELL_DELTA * NUM_GUESSES / 2
BORDER = "#5d9ab3"


class CellManager:
    """ Displays the Wordle cells as tkinter Labels """

    def __init__(self):
        self.cells = []
        self.cur_row = 0
        self.cur_col = 0

        canvas = Canvas(config.window, bg="white", height=300, width=300)
        canvas.config()
        canvas.pack(padx=20, pady=20, side=tkinter.TOP)

        for j in range(0, NUM_GUESSES):
            row = []
            for i in range(0, WORD_LENGTH):
                label = Label(canvas, width=4, height=2, highlightbackground=BORDER, highlightthickness=2,
                              font=('Arial', 16, 'bold'), bg="white")
                label.grid(row=j, column=i, padx=5, pady=5)
                row.append(label)
            self.cells.append(row)

    def process_letter(self, char):
        """ tests if there is space to add a letter to the current word.
        If there is, display the letter in the next cell."""
        if self.cur_row < 6 and self.cur_col < 5:
            self.cells[self.cur_row][self.cur_col].config(text=char.upper())
            self.cur_col += 1
            return True
        return False

    def update_cell_status(self, col, new_color):
        """ Set cell's color """
        self.cells[self.cur_row][col].config(bg=new_color)

    def reset_for_next_word(self):
        """ sets row counter to next word and column's to 0 """
        self.cur_row += 1
        self.cur_col = 0

    def clear_letter(self):
        """ removes last letter from the word being entered """
        self.cur_col -= 1
        self.cells[self.cur_row][self.cur_col].config(text="")
