import tkinter as tk
import random

def generate_random_button_name():
    adjectives = ["Awesome", "Fantastic", "Glorious", "Magical", "Spectacular"]
    nouns = ["Button", "Widget", "Clicker", "Portal", "Trigger"]

    random_adjective = random.choice(adjectives)
    random_noun = random.choice(nouns)

    return f"{random_adjective} {random_noun}"

def button1_click():
    print(f"Button 1 clicked: {button1['text']}")

def button2_click():
    print(f"Button 2 clicked: {button2['text']}")

root = tk.Tk()
root.title("Random Buttons")

button1 = tk.Button(root, text=generate_random_button_name(), command=button1_click)
button1.pack()

button2 = tk.Button(root, text=generate_random_button_name(), command=button2_click)
button2.pack()

root.mainloop()
