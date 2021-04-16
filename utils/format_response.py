import json
from http import HTTPStatus


def format_response(statusCode, message, data=None):
    if HTTPStatus.OK.value >= statusCode and statusCode <= HTTPStatus.ALREADY_REPORTED.value:
        body = {"statusCode": statusCode, "data": data, "message": message}
    else:
        body = {
            "error": {"code": 0, "message": message},
            "data": [],
            "status": statusCode,
        }

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
