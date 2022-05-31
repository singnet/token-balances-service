from datetime import date

from constants.entity import CardanoDBSyncApiResponseEntities
from constants.status import CreatedBy
from domain.factory.snapshot_factory import SnapshotFactory
from infrastructure.models import TokenDBModel, SnapshotHistoryDBModel, CardanoSnapshots
from infrastructure.repository.base_repository import BaseRepository
from utils.general import get_uuid, datetime_in_utcnow


class SnapshotRepository(BaseRepository):

    def get_all_tokens(self, blockchain_name):
        tokens_query = self.session.query(TokenDBModel.row_id, TokenDBModel.id, TokenDBModel.name,
                                          TokenDBModel.blockchain_name, TokenDBModel.description, TokenDBModel.symbol,
                                          TokenDBModel.token_address, TokenDBModel.allowed_decimal,
                                          TokenDBModel.is_enabled, TokenDBModel.created_by, TokenDBModel.created_at,
                                          TokenDBModel.updated_at) \
            .filter(TokenDBModel.is_enabled.is_(True)) \
            .order_by(TokenDBModel.blockchain_name.asc(),
                      TokenDBModel.symbol.asc())

        if blockchain_name:
            tokens_query = tokens_query.filter(TokenDBModel.blockchain_name == blockchain_name)

        tokens = tokens_query.all()

        return [SnapshotFactory.token(row_id=token.row_id, id=token.id, name=token.name,
                                      blockchain_name=token.blockchain_name, description=token.description,
                                      symbol=token.symbol, token_address=token.token_address,
                                      allowed_decimal=token.allowed_decimal, is_enabled=token.is_enabled,
                                      created_by=token.created_by, created_at=token.created_at,
                                      updated_at=token.updated_at) for token in tokens]

    def create_snapshot_history(self, token_id: int, status: str, snapshot_date: date, snapshot_type: str,
                                created_by: str):
        snapshot_history_item = SnapshotHistoryDBModel(id=get_uuid(), token_id=token_id, status=status, address_count=0,
                                                       snapshot_date=snapshot_date, snapshot_type=snapshot_type,
                                                       created_by=created_by, created_at=datetime_in_utcnow(),
                                                       updated_at=datetime_in_utcnow())
        self.add_item(snapshot_history_item)

        return SnapshotFactory.snapshot_history(row_id=snapshot_history_item.row_id, id=snapshot_history_item.id,
                                                token_id=snapshot_history_item.token_id,
                                                status=snapshot_history_item.status,
                                                address_count=snapshot_history_item.address_count,
                                                snapshot_date=snapshot_history_item.snapshot_date,
                                                snapshot_type=snapshot_history_item.snapshot_type,
                                                created_by=snapshot_history_item.created_by,
                                                created_at=snapshot_history_item.created_at,
                                                updated_at=snapshot_history_item.updated_at)

    def add_snapshot(self, snapshot_id: int, token_holders: list):
        snapshot_items = list()
        for token_holder in token_holders:
            snapshot_items.append(CardanoSnapshots(id=get_uuid(), snapshot_id=snapshot_id, address=token_holder.get(
                CardanoDBSyncApiResponseEntities.ADDRESS.value), stake_key=token_holder.get(
                CardanoDBSyncApiResponseEntities.STAKE_KEY.value), balance=token_holder.get(
                CardanoDBSyncApiResponseEntities.BALANCE.value), created_by=CreatedBy.BACKEND.value,
                                                   created_at=datetime_in_utcnow(),
                                                   updated_at=datetime_in_utcnow()))
        if len(snapshot_items):
            self.add_all_items(snapshot_items)

    def update_snapshot_history(self, row_id: int, status: str, address_count: int):
        snapshot_history = self.session.query(SnapshotHistoryDBModel) \
            .filter(SnapshotHistoryDBModel.row_id == row_id).one()

        snapshot_history.status = status
        snapshot_history.address_count = address_count
        snapshot_history.updated_at = datetime_in_utcnow()

        self.session.commit()
