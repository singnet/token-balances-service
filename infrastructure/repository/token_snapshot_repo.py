from datetime import date

from constants.entity import CardanoDBSyncApiResponseEntities
from infrastructure.repository.base_repository import BaseRepository
from infrastructure.models import Snapshots, TransferInfo, StakingTokenSnapshot, TokenDBModel, SnapshotHistoryDBModel, \
    CardanoBalanceDBModel
from domain.factory.token_snapshot_factory import TokenSnapshotFactory
from sqlalchemy import exc

from utils.general import get_uuid, datetime_in_utcnow


class TokenSnapshotRepo(BaseRepository):

    def get_token_balance(self, address):

        address = address.lower()

        try:
            result = (
                self.session.query(Snapshots)
                    .filter(Snapshots.address == address)
                    .first()
            )
            self.session.commit()
        except exc.SQLAlchemyError as e:
            self.session.rollback()
            raise e

        if result is not None:
            transfer_details = self.get_transfer_status(address)
            token_snapshot = TokenSnapshotFactory.convert_token_snapshot_db_to_entity_model(result.address,
                                                                                            result.balance_in_cogs,
                                                                                            result.block_number,
                                                                                            result.snapshot_date)
            token_snapshot.token_transfer_details = transfer_details
        else:
            token_snapshot = TokenSnapshotFactory.convert_token_snapshot_db_to_entity_model(address, 0, 0, '')

        staker_details = self.get_staker_status(address)
        token_snapshot.staker_transfer_details = staker_details

        return token_snapshot.to_response()

    def get_staker_status(self, address):
        try:
            result = (
                self.session.query(StakingTokenSnapshot)
                    .filter(StakingTokenSnapshot.staker_address == address)
                    .first()
            )
            self.session.commit()
        except exc.SQLAlchemyError as e:
            self.session.rollback()
            raise e

        return result or None

    def get_transfer_status(self, address):
        try:
            result = (
                self.session.query(TransferInfo)
                    .filter(TransferInfo.wallet_address == address)
                    .filter(TransferInfo.transfer_status == "SUCCESS")
                    .first()
            )
            self.session.commit()
        except exc.SQLAlchemyError as e:
            self.session.rollback()
            raise e

        return result or None

    def get_all_tokens(self, blockchain_name):
        tokens_query = self.session.query(TokenDBModel.row_id, TokenDBModel.id, TokenDBModel.name,
                                          TokenDBModel.blockchain_name, TokenDBModel.description, TokenDBModel.symbol,
                                          TokenDBModel.token_address, TokenDBModel.balance_types,
                                          TokenDBModel.allowed_decimal,
                                          TokenDBModel.is_enabled, TokenDBModel.created_by, TokenDBModel.created_at,
                                          TokenDBModel.updated_at) \
            .filter(TokenDBModel.is_enabled.is_(True)) \
            .order_by(TokenDBModel.blockchain_name.asc(), TokenDBModel.symbol.asc())

        if blockchain_name:
            tokens_query = tokens_query.filter(TokenDBModel.blockchain_name == blockchain_name)

        tokens = tokens_query.all()

        return [TokenSnapshotFactory.token(row_id=token.row_id, id=token.id, name=token.name,
                                           blockchain_name=token.blockchain_name, description=token.description,
                                           symbol=token.symbol, token_address=token.token_address,
                                           balance_types=token.balance_types,
                                           allowed_decimal=token.allowed_decimal, is_enabled=token.is_enabled,
                                           created_by=token.created_by, created_at=token.created_at,
                                           updated_at=token.updated_at) for token in tokens]

    def create_snapshot_history(self, token_id: int, status: str, snapshot_date: date, snapshot_type: str,
                                created_by: str):
        snapshot_history_item = SnapshotHistoryDBModel(id=get_uuid(), token_id=token_id, status=status, address_count=0,
                                                       delta_count=0, snapshot_date=snapshot_date,
                                                       snapshot_type=snapshot_type, created_by=created_by,
                                                       created_at=datetime_in_utcnow(), updated_at=datetime_in_utcnow())
        self.add_item(snapshot_history_item)

        return TokenSnapshotFactory.snapshot_history(row_id=snapshot_history_item.row_id, id=snapshot_history_item.id,
                                                     token_id=snapshot_history_item.token_id,
                                                     status=snapshot_history_item.status,
                                                     address_count=snapshot_history_item.address_count,
                                                     delta_count=snapshot_history_item.delta_count,
                                                     snapshot_date=snapshot_history_item.snapshot_date,
                                                     snapshot_type=snapshot_history_item.snapshot_type,
                                                     created_by=snapshot_history_item.created_by,
                                                     created_at=snapshot_history_item.created_at,
                                                     updated_at=snapshot_history_item.updated_at)

    def update_snapshot_history(self, row_id: int, status: str, address_count: int, delta_count: int):
        snapshot_history = self.session.query(SnapshotHistoryDBModel) \
            .filter(SnapshotHistoryDBModel.row_id == row_id).one()

        snapshot_history.status = status
        snapshot_history.address_count = address_count
        snapshot_history.delta_count = delta_count
        snapshot_history.updated_at = datetime_in_utcnow()

        self.session.commit()

    def get_token_holders(self, token_id: int, balance_type: str):
        token_holders = self.session.query(CardanoBalanceDBModel.row_id, CardanoBalanceDBModel.id,
                                           CardanoBalanceDBModel.token_id,
                                           CardanoBalanceDBModel.address, CardanoBalanceDBModel.stake_key,
                                           CardanoBalanceDBModel.balance,
                                           CardanoBalanceDBModel.balance_type, CardanoBalanceDBModel.created_by,
                                           CardanoBalanceDBModel.created_at, CardanoBalanceDBModel.updated_at) \
            .filter(CardanoBalanceDBModel.token_id == token_id,
                    CardanoBalanceDBModel.balance_type == balance_type).all()

        return [TokenSnapshotFactory.cardano_balance(row_id=token_holder.row_id, id=token_holder.id,
                                                     token_id=token_holder.token_id, address=token_holder.address,
                                                     stake_key=token_holder.stake_key,
                                                     balance=token_holder.balance,
                                                     balance_type=token_holder.balance_type,
                                                     created_by=token_holder.created_by,
                                                     created_at=token_holder.created_at,
                                                     updated_at=token_holder.updated_at) for token_holder in
                token_holders]

    def insert_token_holders(self, token_id: int, token_holders: list, balance_type: str, created_by: str):
        token_holders_items = list()
        for token_holder in token_holders:
            token_holders_items.append(CardanoBalanceDBModel(id=get_uuid(), token_id=token_id, address=token_holder.get(
                CardanoDBSyncApiResponseEntities.ADDRESS.value), stake_key=token_holder.get(
                CardanoDBSyncApiResponseEntities.STAKE_KEY.value), balance=token_holder.get(
                CardanoDBSyncApiResponseEntities.QUANTITY.value), balance_type=balance_type, created_by=created_by,
                                                             created_at=datetime_in_utcnow(),
                                                             updated_at=datetime_in_utcnow()))
        self.add_all_items(token_holders_items)

    def delete_token_holders(self, token_id: int, token_holders: list, balance_type: str):
        self.session.query(CardanoBalanceDBModel) \
            .filter(CardanoBalanceDBModel.token_id == token_id, CardanoBalanceDBModel.balance_type == balance_type,
                    CardanoBalanceDBModel.address.in_(token_holders)) \
            .delete()
