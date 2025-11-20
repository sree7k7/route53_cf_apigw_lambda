import json
import random

def generate_random_button_name():
    adjectives = ["Awesome", "Fantastic", "Glorious", "Magical", "Spectacular"]
    nouns = ["Button", "Widget", "Clicker", "Portal", "Trigger"]

    random_adjective = random.choice(adjectives)
    random_noun = random.choice(nouns)

    return f"{random_adjective} {random_noun}"

def lambda_handler(event, context):
    button1_name = generate_random_button_name()
    button2_name = generate_random_button_name()

    response = {
        "statusCode": 200,
        "body": json.dumps({
            "button1": button1_name,
            "button2": button2_name
        })
    }
    return response
