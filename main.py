import pandas
from playsound import playsound
import csv
from csv import DictWriter


BACKGROUND_COLOR = "#B1DDC6"
import random
from tkinter import *
import pandas as pd
to_learn = {}
current_card = {}
to_spoof = {}
a_spoof = {}
b_spoof = {}

try: # try running this line of code
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    # If for the first time we are running it
    # the words_to_learn.csv file might not be present
    # and FileNotFoundError might pop up
    original_data = pandas.read_csv("chinese_words.csv")
    #print(original_data)
    to_learn = original_data.to_dict(orient="records")
    to_spoof = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
    to_spoof = data.to_dict(orient="records")
# data = pd.read_csv("./data/words_to_learn.csv")
# word_dict = {row.Chinese:row.English for (index, row) in df.iterrows()}
# spits out a list of dictionaries containing chinese word and english translation
# print(word_dict)


#------------------------ Generating a Chinese word ----------

def next_card():
    global current_card, a_spoof, b_spoof, flip_timer, pos, correct_file
    window.after_cancel(flip_timer)
    
    # Pairs answer with random spoof answers
    current_card = random.choice(to_learn)
    a_spoof = random.choice(to_spoof)
    b_spoof = random.choice(to_spoof)
    
    # chinese_word = random_pair['Chinese']
    canvas.itemconfig(card_title, text="Chinese", fill="black")
    canvas.itemconfig(card_word, text=current_card["Chinese"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)

    #flip_timer = window.after(5000, func=mid_card) ----don't want it to flip right now----
    
    # Sticky and pos will be used when image buttons are working
    sticky=[E, W, S]
    pos=(''.join(random.sample(sticky,len(sticky))))
    

    #----A Spoof Button------
    afile = (a_spoof["Pinyin"])
    spoofa_file = PhotoImage(file=afile)
    abutton= Button(buttons, image=spoofa_file, command= wrong)
    abutton.grid(row=6, column=0, sticky=pos[0])
    print(afile)
    
    #----B Spoof Button------
    bfile = (b_spoof["Pinyin"])
    spoofb_file = PhotoImage(file=bfile)
    bbutton= Button(buttons, image=spoofb_file, command= wrong)
    bbutton.grid(row=6, column=1, sticky=pos[1])
    print(bfile)
    
    #----Correct Button------
    cfile= (current_card["Pinyin"])
    correct_file = PhotoImage(file=cfile)
    button= Button(buttons, image=correct_file, command= next_card)
    button.grid(row=6, column=2, sticky=pos[2])
    print(cfile)
  
    
def wrong():
    canvas.itemconfig(card_title, text = "Wrong", fill = "white")
    canvas.itemconfig(card_word, text=current_card["Chinese"], fill = "white")
    canvas.itemconfig(card_background, image=card_back_img)
    flip_timer = window.after(5000, func=next_card)
    #next_card()

##def tracker():
##    headersCSV = ['ID', 'Pinyin', 'English', 'Chinese', 'Wrong_Pinyin', 'Wrong_English']
##    dict = {'Pinyin':current_card["Pinyin"], 'English':current_card["English"], 'Chinese':current_card["Chinese"]}                 
##
##    with open('tracker.csv', 'a', newline='') as f_object:
##        dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
##        dictwriter_object.writerow(dict)
##        #myfile = csv.writer(file)
##        #myfile.writerow(flipped)
##        f_object.close()

def flip_card():
    canvas.itemconfig(card_title, text = "English", fill = "white")
    canvas.itemconfig(card_word, text=current_card["English"], fill = "white")
    canvas.itemconfig(card_background, image=card_back_img)

def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    #index = false #discrads the index numbers
    next_card()
#------------------------ FlashCard UI Setup -------------------------------

window = Tk()
window.title("Flashcard App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(5000, func=next_card) # 5000 milliseocnds = 5 seconds

canvas = Canvas(width=200, height=125)
card_front_img = PhotoImage(file="./card_front.png")
card_back_img = PhotoImage(file="./card_back.png")

card_background = canvas.create_image(150, 75, image=card_front_img)
card_title = canvas.create_text(100, 50, text="Title", font=("Ariel", 16, "italic"))
# Positions are related to canvas so 400 will be halfway in width
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_word = canvas.create_text(100, 75, text="Word", font=("Ariel", 20, "bold"), tags="word")
# canvas should go in the middle
canvas.grid(row=0, column=1, columnspan=4)

#------------------------ MC Button Setup -------------------------------
buttons = Canvas(width=200, height=100)
buttons.grid(row=4, column=1, columnspan=2)

#------------------------ Simple image button tests -------------------------------
##cross_image = PhotoImage(file="./wrong.png")
##unknown_button = Button(image=cross_image, command = next_card)
##unknown_button.grid(row=4, column=1, sticky="W")
##
##check_image = PhotoImage(file="./right.png")
##known_button = Button(image=check_image, command=is_known)
##known_button.grid(row=4, column=1, sticky="E")

next_card()
window.mainloop()

