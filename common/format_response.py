import json


def format_response(statusCode, message, data=None):

    body = {
        "statusCode": statusCode,
        "data": data,
        "message": message
    }

    response = {
        "statusCode": statusCode,
        "body": json.dumps(body)
    }

    return response
