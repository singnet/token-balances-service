from http import HTTPStatus

from application.services.snapshot_service import SnapshotService
from common.logger import get_logger
from common.utils import generate_lambda_response, make_response_body
from config import SLACK_HOOK, SNAPSHOT_PRUNE_NUMBER
from constants.error_details import ErrorCode, ErrorDetails
from constants.lambdas import LambdaResponseStatus
from utils.exception_handler import exception_handler
from utils.exceptions import EXCEPTIONS, BadRequestException
from utils.lambdas import make_error_format

logger = get_logger(__name__)
snapshot_service = SnapshotService()


@exception_handler(EXCEPTIONS=EXCEPTIONS, SLACK_HOOK=SLACK_HOOK, logger=logger)
def prune_snapshots(event, context):
    logger.info("Started pruning the snapshot history")

    if not SNAPSHOT_PRUNE_NUMBER or SNAPSHOT_PRUNE_NUMBER > 0:
        logger.info(f"Snapshot prune number={SNAPSHOT_PRUNE_NUMBER} is empty or equal to zero")
        raise BadRequestException(error_code=ErrorCode.PROPERTY_VALUES_EMPTY.value,
                                  error_details=ErrorDetails[ErrorCode.PROPERTY_VALUES_EMPTY.value].value)

    response = snapshot_service.prune_snapshots(prune_number=SNAPSHOT_PRUNE_NUMBER)

    return generate_lambda_response(HTTPStatus.OK.value,
                                    make_response_body(status=LambdaResponseStatus.SUCCESS.value, data=response,
                                                       error=make_error_format()), cors_enabled=True)


@exception_handler(EXCEPTIONS=EXCEPTIONS, SLACK_HOOK=SLACK_HOOK, logger=logger)
def create_snapshot(event, context):
    logger.info("Started creating the snapshot")
    response = snapshot_service.create_snapshot()

    return generate_lambda_response(HTTPStatus.OK.value,
                                    make_response_body(status=LambdaResponseStatus.SUCCESS.value, data=response,
                                                       error=make_error_format()), cors_enabled=True)


print(create_snapshot({}, {}))
