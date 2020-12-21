import tkinter as tk
from import_words import words_list, languages_list
import random
import pandas as pd


BACKGROUND_COLOR = "#B1DDC6"
PADDING_AMOUNT_WINDOW = 50
PADDING_AMOUNT_CARD = 20
CARD_HEIGHT = 526
CARD_WIDTH = 800
RESIZE_MULTIPLE = 2
CARD_WIDTH /= RESIZE_MULTIPLE
CARD_HEIGHT /= RESIZE_MULTIPLE
FONT_TITLE = ("Arial", 20, "italic")
FONT_WORD = ("Arial", 40, "bold")
UNIT_TIME_MS = 10 ** 3
timer_var = None
languages_ord = 0
TIME_ALLOWED = 7 # How long card stays on screen before flipping (secs)
word_dict = None


window = tk.Tk()
window.config(padx=PADDING_AMOUNT_WINDOW, pady=PADDING_AMOUNT_WINDOW, bg=BACKGROUND_COLOR)
window.title("Flash Cards")
window.resizable(True, True)

canvas_card = tk.Canvas(width=CARD_WIDTH, height=CARD_HEIGHT, bg=BACKGROUND_COLOR, highlightthickness=0)
orig_card_back_image = tk.PhotoImage(file=r".\images\card_back.png")
orig_card_front_image = tk.PhotoImage(file=r".\images\card_front.png")
# Reduce image size for smaller screen 13"
display_card_front_image = orig_card_front_image.subsample(x=RESIZE_MULTIPLE, y=RESIZE_MULTIPLE)
display_card_back_image = orig_card_back_image.subsample(x=RESIZE_MULTIPLE, y=RESIZE_MULTIPLE)
display_cards = [display_card_front_image, display_card_back_image]
fg_cards = ["black", "white"]
canvas_card_image = canvas_card.create_image(CARD_WIDTH/2, CARD_HEIGHT/2, image=display_cards[languages_ord])
card_title = canvas_card.create_text(CARD_WIDTH/2, CARD_HEIGHT/4, text="", font=FONT_TITLE, fill=fg_cards[languages_ord])
card_word = canvas_card.create_text(CARD_WIDTH/2, CARD_HEIGHT*0.6, text="", font=FONT_WORD, fill=fg_cards[languages_ord])
canvas_card.grid(row=0, column=0, columnspan=2, padx=PADDING_AMOUNT_CARD, pady=PADDING_AMOUNT_CARD)
# -----------------------------------------------------
# ------------ NEW WORD Function ----------------------
def new_word():
    random.seed()
    random_word = random.choice(words_list)
    return random_word
def next_card():
    global word_dict
    word_dict = new_word()
    language_ord = 0
    language = languages_list[language_ord]
    format_card(word_dict)
    start_flip(word_dict)
# --------------- KNOWN BUTTON ------------------------
def known_command():
    if timer_var is not None:
        words_list.remove(word_dict)
        df = pd.DataFrame(words_list)
        df.to_csv(r".\data\words_to_learn.csv", index=False)
        window.after_cancel(timer_var)
    next_card()

right_image = tk.PhotoImage(file=r".\images\right.png")
known_button = tk.Button(image=right_image, highlightthickness=0, command=known_command)
known_button.grid(row=1, column=1)
# -----------------------------------------------------
# -------------- UNKNOWN BUTTON -----------------------
def unknown_command():
    if timer_var is not None:
        window.after_cancel(timer_var)
    next_card()


wrong_image = tk.PhotoImage(file=r".\images\wrong.png")
unknown_button = tk.Button(image=wrong_image, highlightthickness=0, command=unknown_command)
unknown_button.grid(row=1, column=0)
# -----------------------------------------------------
# ----------------- FLIP CARD -------------------------


def format_card(word_dict_x):
    global languages_ord
    canvas_card.itemconfig(canvas_card_image, image=display_cards[languages_ord])
    canvas_card.itemconfig(card_title, text=languages_list[languages_ord], fill=fg_cards[languages_ord])
    canvas_card.itemconfig(card_word, text=word_dict_x[languages_list[languages_ord]], fill=fg_cards[languages_ord])


def start_flip(word_dict_x):
    flip_card(TIME_ALLOWED, word_dict_x)


def flip_card(remaining_secs, word_dict_x):
    global timer_var, languages_ord
    if remaining_secs > 0:
        timer_var = window.after(UNIT_TIME_MS, flip_card, remaining_secs - 1, word_dict_x)
    else:
        # Flip Card
        if languages_ord == 0:
            languages_ord = 1
        else:
            languages_ord = 0
        format_card(word_dict_x)
        # Initialise Flip Timer
        start_flip(word_dict_x)

next_card()

window.mainloop()
