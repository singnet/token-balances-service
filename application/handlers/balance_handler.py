import json

from utils.format_response import format_response
from jsonschema import validate, ValidationError
from application.services.balance_service import find_snapshot_by_address
from http import HTTPStatus


def get_token_balance(event, context):
    data = None
    statusCode = HTTPStatus.BAD_REQUEST.value

    schema = {
        "type": "object",
        "properties": {"wallet_address": {"type": "string"}},
        "required": ["wallet_address"],
    }

    try:
        inputs = event["body"] or None
        if inputs is None:
            message = HTTPStatus.BAD_REQUEST.phrase
        else:
            payload = json.loads(inputs)
            validate(instance=payload, schema=schema)
            statusCode, message, data = find_snapshot_by_address(
                payload["wallet_address"]
            )
    except ValidationError as e:
        message = e.message

    return format_response(statusCode, message, data)
