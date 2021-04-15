import json


def format_response(statusCode, message, data=None):

    body = {"statusCode": statusCode, "data": data, "message": message}

    response = {
        "headers": {
            "Access-Control-Allow-Headers": "Access-Control-Allow-Origin, Content-Type, X-Amz-Date, Authorization",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS,POST",
        },
        "statusCode": statusCode,
        "body": json.dumps(body),
    }

    return response
