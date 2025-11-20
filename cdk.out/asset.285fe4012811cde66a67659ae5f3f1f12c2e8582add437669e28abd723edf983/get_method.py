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
import slack_sdk

def create_button():
    button = {
        "type": "button",
        "action_id": "hello_button",
        "text": {
            "type": "plain_text",
            "text": "Hello",
            "emoji": True
        }
    }

    # client = slack_sdk.WebClient(token='your-slack-token')
    # response = client.chat_postMessage(
    #     channel='your-channel-id',
    #     text='Button created',
    #     attachments=[{'blocks': [button]}]
    # )

    # return response