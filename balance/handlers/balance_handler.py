from common.format_response import format_response


def get_token_balance(event, context):
    statusCode = 200
    message = "Success"
    body = {
        "wallet_address": "0x",
        "balance_in_cogs": 100,
        "snapshot_date": "2020-01-04",
        "conversion_transaction": {
            "converted_tokens": 100,
            "transfer_time": "2020-01-05",
            "transaction_hash": "0x",
        },
    }

    return format_response(statusCode, message, data=body)
