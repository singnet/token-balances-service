import itertools
from datetime import date
from http import HTTPStatus

from application.services.cardano_db_sync_service import CardanoDBSyncService
from application.services.response.balance_service_response import get_available_tokens_response_format, \
    create_snapshot_history_response_format, get_token_holders_response_format, \
    existing_token_holders_response_format, process_update_token_balance_response_format, \
    update_token_balance_response_format
from common.logger import get_logger
from common.utils import Utils
from config import SLACK_HOOK
from constants.entity import TokenEntities, CardanoDBSyncApiResponseEntities, APIStatusResponse, \
    SnapshotHistoryEntities, UpdateTokenBalanceEntity
from constants.error_details import ErrorCode, ErrorDetails
from constants.general import ALLOWED_BALANCE_TYPES
from constants.status import SnapshotHistoryStatus, CreatedBy
from infrastructure.repository.token_snapshot_repo import TokenSnapshotRepo
from utils.exceptions import InternalServerErrorException
from utils.general import get_response_from_entities, datetime_in_utcnow, datetime_to_str

logger = get_logger(__name__)


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


class BalanceService:

    def __init__(self):
        self.token_repo = TokenSnapshotRepo()

    def get_available_tokens(self, blockchain_name=None):
        logger.info(f"Getting the available tokens for the blockchain_name={blockchain_name}")
        tokens = self.token_repo.get_all_tokens(blockchain_name=blockchain_name)
        return get_available_tokens_response_format(get_response_from_entities(tokens))

    def create_snapshot_history(self, token_id: int, status: str, snapshot_date: date, snapshot_type: str,
                                created_by: str):
        logger.info(
            f"Creating the snapshot history with token_id={token_id}, status={status}, "
            f"snapshot_date={datetime_to_str(snapshot_date)}, "
            f"snapshot_type={snapshot_type}, created_by={created_by}")
        snapshot_history = self.token_repo.create_snapshot_history(token_id=token_id, status=status,
                                                                   snapshot_date=snapshot_date,
                                                                   snapshot_type=snapshot_type,
                                                                   created_by=created_by)

        return create_snapshot_history_response_format(snapshot_history=snapshot_history.to_dict())

    def update_snapshot_history(self, row_id: int, status: str, address_count: int, delta_count: int):
        logger.info(
            f"Updating the snapshot history for the row_id={row_id} with status={status}, "
            f"address_count={address_count}, delta_count={delta_count}")
        self.token_repo.update_snapshot_history(row_id=row_id, status=status, address_count=address_count,
                                                delta_count=delta_count)

    def get_token_holders(self, token_id: int, balance_type: str):
        logger.info(f"Getting the token holders for the token_id={token_id}, balance_type={balance_type}")
        token_holders = self.token_repo.get_token_holders(token_id=token_id, balance_type=balance_type)
        return get_token_holders_response_format(get_response_from_entities(token_holders))

    def insert_token_holders(self, token_id: int, token_holders: list, balance_type: str):
        logger.info(
            f"Adding the token holders for the token_id={token_id}, balance_type={balance_type} of "
            f"total holders={len(token_holders)}")
        self.token_repo.insert_token_holders(token_id=token_id, token_holders=token_holders, balance_type=balance_type,
                                             created_by=CreatedBy.BACKEND.value)

    def delete_token_holders(self, token_id: int, token_holders: list, balance_type: str):
        logger.info(
            f"Deleting the token holders for the token_id={token_id}, balance_type={balance_type} of "
            f"total holders={len(token_holders)}")
        delete_holders = [token_holder.get(CardanoDBSyncApiResponseEntities.ADDRESS.value) for token_holder in
                          token_holders]
        self.token_repo.delete_token_holders(token_id=token_id, token_holders=delete_holders, balance_type=balance_type)

    def process_update_token_balance(self, token_id, balance_type, current_holders):
        existing_token_holders = self.get_token_holders(token_id=token_id, balance_type=balance_type)
        previous_holders = existing_token_holders_response_format(existing_token_holders)

        delete_token_holders = list(itertools.filterfalse(lambda x: x in current_holders, previous_holders))
        insert_token_holders = list(itertools.filterfalse(lambda x: x in previous_holders, current_holders))

        print(delete_token_holders)
        print(insert_token_holders)

        self.delete_token_holders(token_id=token_id, token_holders=delete_token_holders, balance_type=balance_type)
        self.insert_token_holders(token_id=token_id, token_holders=insert_token_holders, balance_type=balance_type)

        delete_token_holders_len = len(delete_token_holders)
        insert_token_holders_len = len(insert_token_holders)
        previous_holders_len = len(previous_holders)

        return process_update_token_balance_response_format(
            delta_count=delete_token_holders_len + insert_token_holders_len, insert_count=insert_token_holders_len,
            delete_count=delete_token_holders_len,
            current_count=previous_holders_len + insert_token_holders_len - delete_token_holders_len)

    @staticmethod
    def get_current_token_holders_balance(token_address, token_symbol, balance_type):
        logger.info(f"Getting the current token holders for the token_address={token_address}, "
                    f"token_symbol={token_symbol}, balance_type={balance_type}")
        token_holders_response = CardanoDBSyncService.get_asset_holders(policy_id=token_address,
                                                                        asset_name=token_symbol)

        if token_holders_response.get(
                CardanoDBSyncApiResponseEntities.STATUS.value) != APIStatusResponse.SUCCESS.value:
            raise InternalServerErrorException(error_code=ErrorCode.API_FAILED.value,
                                               error_details=ErrorDetails[ErrorCode.API_FAILED.value].value)

        return token_holders_response.get(CardanoDBSyncApiResponseEntities.DATA.value, {})

    def trigger_updating_token_balance(self, tokens):
        for token in tokens:
            token_id = token.get(TokenEntities.ROW_ID.value)
            token_address = token.get(TokenEntities.TOKEN_ADDRESS.value)
            token_symbol = token.get(TokenEntities.SYMBOL.value)
            for balance_type in token.get(TokenEntities.BALANCE_TYPES.value):

                if balance_type not in ALLOWED_BALANCE_TYPES:
                    logger.info(f"Skipping the balance_type={balance_type} as it is not allowed yet")
                    continue

                snapshot_history = self.create_snapshot_history(token_id=token.get(TokenEntities.ROW_ID.value),
                                                                status=SnapshotHistoryStatus.STARTED.value,
                                                                snapshot_date=datetime_in_utcnow(),
                                                                snapshot_type=balance_type,
                                                                created_by=CreatedBy.BACKEND.value)
                snapshot_id = snapshot_history.get(SnapshotHistoryEntities.ROW_ID.value)

                try:
                    response_data = BalanceService.get_current_token_holders_balance(token_address=token_address,
                                                                                     token_symbol=token_symbol,
                                                                                     balance_type=balance_type)
                    token_holders = response_data.get(CardanoDBSyncApiResponseEntities.ITEMS.value, [])
                    processed_output = self.process_update_token_balance(token_id=token_id,
                                                                         balance_type=balance_type,
                                                                         current_holders=token_holders)

                    self.update_snapshot_history(row_id=snapshot_id, status=SnapshotHistoryStatus.FINISHED.value,
                                                 address_count=processed_output.get(
                                                     UpdateTokenBalanceEntity.CURRENT_COUNT.value),
                                                 delta_count=processed_output.get(
                                                     UpdateTokenBalanceEntity.DELTA_COUNT.value))
                    logger.info(f"Updated the token balance for the token_id={token_id}, snapshot_id={snapshot_id}, "
                                f"balance_type={balance_type}, with output={processed_output}")
                except Exception as e:
                    self.update_snapshot_history(row_id=snapshot_id, status=SnapshotHistoryStatus.FAILED.value,
                                                 address_count=0, delta_count=0)
                    message = f"Exception occurred on creating snapshot process={e}"
                    logger.exception(message)
                    Utils().report_slack(slack_msg=message, SLACK_HOOK=SLACK_HOOK)

    def update_token_balance(self):
        logger.info("Update the token balance")
        tokens = self.get_available_tokens()

        if not len(tokens):
            logger.info("No tokens configured in the database")
            return update_token_balance_response_format("No tokens configured in the database")

        self.trigger_updating_token_balance(tokens=tokens)
        logger.info("Updated the token balance successfully")

        return update_token_balance_response_format("Successfully updated the token balance")
