import json

from common.format_response import format_response
from jsonschema import validate, ValidationError
from balance.services.balance_service import find_snapshot_by_address


def get_token_balance(event, context):

    data = None
    statusCode = 400

    schema = {
        "type": "object",
        "properties": {"wallet_address": {"type": "string"}},
        "required": ["wallet_address"],
    }

    try:
        inputs = event["body"] or None
        if inputs is None:
            message = "Bad request"
        else:
            payload = json.loads(inputs)
            validate(instance=payload, schema=schema)
            statusCode, message, data = find_snapshot_by_address(
                payload["wallet_address"]
            )
    except ValidationError as e:
        message = e.message

    return format_response(statusCode, message, data)
