import json

def lambda_handler(event, context):
    # Your button press logic here
    response = {
        "statusCode": 200,
        "body": json.dumps("Button pressed successfully!")
    }
    return response
