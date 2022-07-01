from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

# ---------------------------- FLASH CARDS ------------------------------- #
try:
    data = pandas.read_csv('data/words_to_learn.csv')
except (FileNotFoundError, pandas.errors.EmptyDataError):
    data = pandas.read_csv('data/french_words.csv')

words = pandas.DataFrame.to_dict(data, orient="records")
current_card = {}


def out_of_words():
    window.after_cancel(flip)
    card.itemconfig(card_background, image=card_back_img)
    card.itemconfig(word_text, text="You've mastered every word, restart the program to reset the words.",
                    font=("ariel", "15", "normal"))
    card.itemconfig(title_text, text="🎉 congratulations 🎉")


def remove_card():
    to_learn = words
    to_learn.remove(current_card)
    to_learn = pandas.DataFrame(to_learn)
    to_learn.to_csv('data/words_to_learn.csv', index=False)
    new_card()


def new_card():
    global current_card, flip
    window.after_cancel(flip)
    card.itemconfig(card_background, image=card_front_img)
    try:
        current_card = random.choice(words)
    except IndexError:
        out_of_words()
    else:
        card.itemconfig(title_text, text="French", fill="black")
        card.itemconfig(word_text, text=current_card['French'], fill="black")
        flip = window.after(3000, func=flip_card)


def flip_card():
    card.itemconfig(title_text, text="English", fill="white")
    card.itemconfig(word_text, text=current_card['English'], fill="white")
    card.itemconfig(card_background, image=card_back_img)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("French Flash Card Game")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip = window.after(3000, func=flip_card)

# Cards
card = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = card.create_image(400, 263, image=card_front_img)
title_text = card.create_text(400, 150, text="", fill="black", font=("ariel", "40", "italic"))
word_text = card.create_text(400, 263, text="", fill="black", font=("ariel", "60", "bold"))
card.grid(row=0, column=0, columnspan=2)


# Buttons
wrong_button_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=new_card)
wrong_button.grid(row=1, column=0)

right_button_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_button_img, highlightthickness=0, command=remove_card)
right_button.grid(row=1, column=1)

try:
    new_card()
except pandas.errors.EmptyDataError:
    out_of_words()


window.mainloop()
