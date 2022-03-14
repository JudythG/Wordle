from wordmanager import WordManager
import config
from cellmanager import CellManager
import string
from tkinter import messagebox, Canvas, Button
import tkinter

POSITION_MATCH = 1
LETTER_MATCH = 2
NO_MATCH = 3
COLOR_POSITION_MACH = "green"
COLOR_LETTER_MATCH = "yellow"
COLOR_NO_MATCH = "gray"


# ------------------------------------------------ UPDATE DISPLAY ------------------------------------------------------
def create_keyboard_key(letter, x, y):
    """ Create a keyboard letter (as a button) for the on-screen keyboard display """
    if letter == '\r':
        keyboard_btn = Button(keyboard_canvas, text="Enter", font=('Arial', 10, 'bold'),
                              command=lambda m=letter: on_click(m))
        keyboard_btn.place(relx=1, x=x, y=y, width=40, height=42, anchor=tkinter.NE)
    elif letter == '\b':
        x -= -45
        keyboard_btn = Button(keyboard_canvas, text="Backspace", font=('Arial', 10, 'bold'),
                              command=lambda m=letter: on_click(m))
        keyboard_btn.place(relx=1, x=x, y=y, width=80, height=42, anchor=tkinter.NE)
    else:
        keyboard_btn = Button(keyboard_canvas, text=letter, font=('Arial', 16, 'bold'),
                              command=lambda m=letter: on_click(m))
        keyboard_btn.place(relx=1, x=x, y=y, width=36, anchor=tkinter.NE)
    keyboard_cells[letter] = keyboard_btn


def set_background_color(column, letter, new_color):
    """ set background color for Wordle cell and on-screen key"""
    cellManager.update_cell_status(column, new_color)
    update_keyboard_cell_status(letter, new_color)


def clear_letter():
    """ remove the last letter from the current word """
    global cur_word
    global cellManager
    if len(cur_word) > 0:
        cur_word = cur_word[:-1]
        cellManager.clear_letter()


def update_keyboard_cell_status(char, color):
    """ update status color of an on-screen keyboard key """
    btn = keyboard_cells.get(char)
    if btn and not btn.cget("bg") == COLOR_POSITION_MACH:
        btn = keyboard_cells[char]
        btn.config(bg=color)


# ------------------------------------------------------ HANDLE INPUT --------------------------------------------------
def on_click(s):
    """ handle click for on-screen keyboard key """
    process_letter(s[0])


def get_letter_from_keypress(e):
    """ handle key-press on keyboard """
    process_letter(e.char.upper())


def process_letter(c):
    """ if letter is ASCII, add it to current word,
        if Return key, test if valid word and update screen as necessary
         if Backspace, remove last letter from current word
    """
    if c in string.ascii_uppercase:
        global cur_word
        if not guessed_word:
            if cellManager.process_letter(c):
                cur_word += c

    # Return key
    elif c == '\r':
        check_word()

    # Backspace
    elif c == '\b':
        clear_letter()


def check_word():
    """ handles word validation """
    global cur_word, guessed_word

    if len(cur_word) == 5:
        if wordManager.is_word(cur_word):
            letter_status = [NO_MATCH] * 5
            letter_count = {}
            for letter in final_word:
                if letter not in letter_count:
                    letter_count[letter] = final_word.count(letter);

            for n in range(0, 5):
                if cur_word[n] == final_word[n] or cur_word[n] in letter_count:
                    if cur_word[n] == final_word[n]:
                        set_background_color(n, cur_word[n], COLOR_POSITION_MACH)
                    elif cur_word[n] in letter_count:
                        set_background_color(n, cur_word[n], COLOR_LETTER_MATCH)
                    letter_status[n] = POSITION_MATCH
                    letter_count[cur_word[n]] -= 1
                    if letter_count[cur_word[n]] == 0:
                        del letter_count[cur_word[n]]
                else:
                    set_background_color(n, cur_word[n], COLOR_NO_MATCH)
            if cur_word == final_word:
                guessed_word = True
                messagebox.showinfo("Congrats!", "You found the word.")
            elif cellManager.cur_row == 5:
                messagebox.showinfo(title="Ouch!", message=f"The word was {final_word}")
            cellManager.reset_for_next_word()
            cur_word = ""
        else:
            messagebox.showinfo("Oops!", f"{cur_word} is not a valid word.")


# --------------------------------------------------- INITIALIZATION ---------------------------------------------------
config.window.bind("<Key>", get_letter_from_keypress)
cur_word = ""
guessed_word = False
cellManager = CellManager()
wordManager = WordManager()
final_word = wordManager.get_random_word()
if final_word:
    print(final_word)

# --------------------------------------------- DISPLAY ONSCREEN KEYBOARD ----------------------------------------------
keyboard_cells = {}
keyboard_x_start = [-419, -396, -419]
keyboard_y_start = [0, 50, 100]
keyboard_x_delta = -46

keyboard_canvas = Canvas(config.window, bg="white", height=200, width=500, highlightthickness=0)
keyboard_canvas.config()
keyboard_canvas.pack(pady=20, side=tkinter.BOTTOM)

qwerty_keyboard = ['QWERTYUIOP', 'ASDFGHJKL', '\rZXCVBNM\b']
for j in range(0, len(qwerty_keyboard)):
    keyboard_row = qwerty_keyboard[j]
    cur_x = keyboard_x_start[j]
    cur_y = keyboard_y_start[j]
    for i in range(0, len(keyboard_row)):
        create_keyboard_key(keyboard_row[i], cur_x, cur_y)
        cur_x -= keyboard_x_delta


config.window.mainloop()
