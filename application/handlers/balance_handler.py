import json

from common.utils import logger, generate_lambda_response, make_response_body
from config import SLACK_HOOK
from constants.lambdas import LambdaResponseStatus
from utils.exception_handler import exception_handler
from utils.exceptions import EXCEPTIONS
from utils.format_response import format_response
from jsonschema import validate, ValidationError
from application.services.balance_service import get_snapshot_by_address, BalanceService
from http import HTTPStatus

from utils.general import get_uuid
from utils.lambdas import make_error_format

balance_service = BalanceService()


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
            statusCode, message, data = get_snapshot_by_address(
                payload["wallet_address"]
            )
    except ValidationError as e:
        message = e.message

    return format_response(statusCode, message, data)


@exception_handler(EXCEPTIONS=EXCEPTIONS, SLACK_HOOK=SLACK_HOOK, logger=logger)
def update_token_balance(event, context):
    logger.info("Started updating the token balance handler")
    response = balance_service.update_token_balance()

    return generate_lambda_response(HTTPStatus.OK.value,
                                    make_response_body(status=LambdaResponseStatus.SUCCESS.value, data=response,
                                                       error=make_error_format()), cors_enabled=True)


print(get_uuid())