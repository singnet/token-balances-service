import json

from utils.format_response import format_response
from jsonschema import validate, ValidationError, FormatChecker
from application.services.customer_service import submit_user_question
from http import HTTPStatus


def submit_question(event, context):
    statusCode = HTTPStatus.BAD_REQUEST.value

    schema = {
        "type": "object",
        "properties": {
            "email": {"type": "string", "format": "email"},
            "name": {"type": "string"},
            "wallet_address": {"type": "string"},
            "comment": {"type": "string"},
            "block_number": {"type": "number"},
        },
        "required": ["email", "wallet_address", "comment", "block_number"],
    }

    try:
        inputs = event["body"] or None
        headers = event["headers"]
        signature = headers.get("Authorization") or None
        if inputs is None or signature is None:
            message = HTTPStatus.BAD_REQUEST.phrase
        else:
            payload = json.loads(inputs)
            validate(instance=payload, schema=schema, format_checker=FormatChecker())
            statusCode, message = submit_user_question(payload, signature)
    except ValidationError as e:
        message = e.message

    return format_response(statusCode, message)
