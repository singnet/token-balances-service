from datetime import date

from application.services.cardano_db_sync_service import CardanoDBSyncService
from application.services.response.snapshot_service_response import get_available_tokens_response_format, \
    create_snapshot_history_response_format
from common.logger import get_logger
from constants.entity import TokenEntities, CardanoDBSyncApiResponseEntities, APIStatusResponse, SnapshotHistoryEntities
from constants.error_details import ErrorCode, ErrorDetails
from constants.status import SnapshotHistoryStatus, SnapshotType, CreatedBy
from infrastructure.repository.snapshot_repository import SnapshotRepository
from utils.exceptions import InternalServerErrorException
from utils.general import datetime_in_utcnow, datetime_to_str, get_response_from_entities

logger = get_logger(__name__)


class SnapshotService:

    def __init__(self):
        self.snapshot_repo = SnapshotRepository()

    def get_available_tokens(self, blockchain_name=None):
        logger.info(f"Getting the available tokens for the blockchain_name={blockchain_name}")
        tokens = self.snapshot_repo.get_all_tokens(blockchain_name=blockchain_name)
        return get_available_tokens_response_format(get_response_from_entities(tokens))

    def create_snapshot_history(self, token_id: int, status: str, snapshot_date: date, snapshot_type: str,
                                created_by: str):
        logger.info(
            f"Creating the snapshot history with token_id={token_id}, status={status}, snapshot_date={datetime_to_str(snapshot_date)}, "
            f"snapshot_type={snapshot_type}, created_by={created_by}")
        snapshot_history = self.snapshot_repo.create_snapshot_history(token_id=token_id, status=status,
                                                                      snapshot_date=snapshot_date,
                                                                      snapshot_type=snapshot_type,
                                                                      created_by=created_by)
        return create_snapshot_history_response_format(snapshot_history=snapshot_history)

    def add_snapshot(self, snapshot_id, token_holders):
        logger.info(
            f"Adding the snapshot for the snapshot_id={snapshot_id}, with total token_holders={len(token_holders)}")
        self.snapshot_repo.add_snapshot(snapshot_id, token_holders)

    def update_snapshot_history(self, row_id, status, address_count):
        logger.info(
            f"Updating the snapshot history for the row_id={row_id} with status={status}, address_count={address_count}")
        self.snapshot_repo.update_snapshot_history(row_id=row_id, status=status, address_count=address_count)

    def process_create_snapshot(self, tokens):

        if not len(tokens):
            logger.info("No tokens configured in the database")

        for token in tokens:
            snapshot_time = datetime_in_utcnow()
            snapshot_history = self.create_snapshot_history(token_id=token.get(TokenEntities.ROW_ID.value),
                                                            status=SnapshotHistoryStatus.STARTED.value,
                                                            snapshot_date=snapshot_time,
                                                            snapshot_type=SnapshotType.TOKEN.value,
                                                            created_by=CreatedBy.BACKEND.value)
            snapshot_id = snapshot_history.get(SnapshotHistoryEntities.ROW_ID.value)

            try:
                token_holders_response = CardanoDBSyncService.get_asset_holders(
                    policy_id=token.get(TokenEntities.TOKEN_ADDRESS.value),
                    asset_name=token.get(TokenEntities.SYMBOL.value))

                if token_holders_response.get(
                        CardanoDBSyncApiResponseEntities.STATUS.value) != APIStatusResponse.SUCCESS.value:
                    raise InternalServerErrorException(error_code=ErrorCode.API_FAILED.value,
                                                       error_details=ErrorDetails[ErrorCode.API_FAILED.value].value)

                data = token_holders_response.get(CardanoDBSyncApiResponseEntities.DATA.value, {})
                token_holders = data.get(CardanoDBSyncApiResponseEntities.ITEMS.value, [])
                count = data.get(CardanoDBSyncApiResponseEntities.META.value, {}).get(
                    CardanoDBSyncApiResponseEntities.COUNT.value, 0)

                self.add_snapshot(snapshot_id=snapshot_id, token_holders=token_holders)
                self.update_snapshot_history(row_id=snapshot_id, status=SnapshotHistoryStatus.FINISHED.value,
                                             address_count=count)
            except Exception as e:
                self.update_snapshot_history(row_id=snapshot_id, status=SnapshotHistoryStatus.FAILED.value,
                                             address_count=0)
                logger.exception(f"Exception occurred on creating snapshot process={e}")
                ##  add to do add slack hook

    def process_prune_snapshots(self, tokens: list, prune_number: int):

        if not len(tokens):
            logger.info("No tokens configured in the database")

        for token in tokens:
            prune_snapshots = self.snapshot_repo.get_snapshot_history(token_id=token.get(TokenEntities.ROW_ID.value),
                                                                      status=SnapshotHistoryStatus.FINISHED.value,
                                                                      offset=prune_number)
            # to do delete logic

    def prune_snapshots(self, prune_number):
        logger.info(f"Pruning the snapshot history with number={prune_number}")
        tokens = self.get_available_tokens()
        self.process_prune_snapshots(tokens=tokens, prune_number=prune_number)

    def create_snapshot(self):
        logger.info("Creating the snapshot")
        tokens = self.get_available_tokens()
        self.process_create_snapshot(tokens=tokens)
        return tokens
