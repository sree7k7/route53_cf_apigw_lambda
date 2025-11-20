import os
import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('This is get method from Lambda, creating button!')
    }

# # create a button with name hello
def create_button():
    # create a button with name hello
    button = {
        "type": "button",
        "action_id": "hello_button",
        "text": {
            "type": "plain_text",
            "text": "Hello",
            "emoji": True
        }
    }
    return 'button created', + button