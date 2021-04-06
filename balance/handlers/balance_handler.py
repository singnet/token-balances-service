from common.format_response import format_response
from balance.services.balance_service import get_snapshot_balance


def get_token_balance(event, context):

    schema = {
        "type": "object",
        "properties": {
            "address": {"type": "string"}
        }
    }

    inputs = event['body']

    try:
        validate(instance=inputs, schema=schema)
        statusCode = 200
        message = "Success"
        body = get_snapshot_balance(inputs['address'])
    except ValidationError as e:
        statusCode = 400
        message = "Validation failed"
        body = {
            "errors": e.message
        }

    return format_response(statusCode, message, data=body)
