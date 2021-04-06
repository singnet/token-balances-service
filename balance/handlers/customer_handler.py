import json

from common.format_response import format_response
from jsonschema import validate, ValidationError
from balance.services.customer_service import submit_user_question


def submit_question(event, context):
    statusCode = 400

    schema = {
        "type": "object",
        "properties": {
            "email": {"type": "string"},
            "name": {"type": "string"},
            "wallet_address": {"type": "string"},
            "comment": {"type": "string"},
        },
        "required": ["email", "wallet_address", "comment"],
    }

    try:
        inputs = event["body"] or None
        if inputs is None:
            message = "Bad request"
        else:
            payload = json.loads(inputs)
            validate(instance=payload, schema=schema)

            email = payload["email"]
            wallet_address = payload["wallet_address"]
            comment = payload["comment"]
            name = payload.get("name") or None

            statusCode, message = submit_user_question(
                wallet_address, email, comment, name
            )
    except ValidationError as e:
        message = e.message

    return format_response(statusCode, message)
