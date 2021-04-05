from common.format_response import format_response


def get_token_balance(event, context):
    body = {
        "address": "0x176133a958449C28930970989dB5fFFbEdd9F447",
        "network": "Ropsten"
    }

    return format_response(statusCode=200, message='Success', data=body)
