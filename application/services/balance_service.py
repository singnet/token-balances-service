from infrastructure.repository.token_snapshot_repo import TokenSnapshotRepo
from http import HTTPStatus


def get_snapshot_by_address(address):
    balance = TokenSnapshotRepo().get_token_balance(address)

    if balance is None:
        data = None
        statusCode = HTTPStatus.BAD_REQUEST.value
        message = "Address not found in snapshot"
    else:
        data = balance
        statusCode = HTTPStatus.OK.value
        message = HTTPStatus.OK.phrase

    return statusCode, message, data
