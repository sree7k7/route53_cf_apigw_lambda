import json
import tkinter as tk
import random
from tkinter import PhotoImage

def generate_random_button_name():
    adjectives = ["Awesome", "Fantastic", "Glorious", "Magical", "Spectacular"]
    nouns = ["Button", "Widget", "Clicker", "Portal", "Trigger"]

    random_adjective = random.choice(adjectives)
    random_noun = random.choice(nouns)

    return f"{random_adjective} {random_noun}"

def lambda_handler(event, context):
    root = tk.Tk()
    root.title("Random Buttons")

    button1_name = generate_random_button_name()
    button2_name = generate_random_button_name()

    def button1_click():
        print(f"Button 1 clicked: {button1_name}")

    def button2_click():
        print(f"Button 2 clicked: {button2_name}")

    button1 = tk.Button(root, text=button1_name, command=button1_click)
    button1.pack()

    button2 = tk.Button(root, text=button2_name, command=button2_click)
    button2.pack()

    root.mainloop()

    response = {
        "statusCode": 200,
        "body": json.dumps("Graphical buttons created successfully!")
    }
    return response
