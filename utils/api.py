import json

import requests

from common.logger import get_logger
from constants.error_details import ErrorCode, ErrorDetails
from constants.status import ApiMethodType
from utils.exceptions import InternalServerErrorException

logger = get_logger(__name__)


def call_api(url: str, method_type: str, data: str = None, headers: dict = None):
    logger.info(f"Calling the api with url={url}, method_type={method_type}, data={data}")
    try:
        if method_type == ApiMethodType.GET.value:
            response = requests.get(url=url, data=data, headers=headers)
        else:
            raise InternalServerErrorException(error_code=ErrorCode.UNEXPECTED_API_METHOD_PROVIDED.value,
                                               error_details=ErrorDetails[
                                                   ErrorCode.UNEXPECTED_API_METHOD_PROVIDED.value].value)

        response = json.loads(response.content.decode("utf-8"))

    except Exception as e:
        logger.exception(f"Unexpected error while calling the cardano db service={e}")
        raise InternalServerErrorException(error_code=ErrorCode.UNEXPECTED_ERROR_ON_CARDANO_DB_SYNC_SERVICE_CALL.value,
                                           error_details=ErrorDetails[
                                               ErrorCode.UNEXPECTED_ERROR_ON_CARDANO_DB_SYNC_SERVICE_CALL.value].value)
    return response
