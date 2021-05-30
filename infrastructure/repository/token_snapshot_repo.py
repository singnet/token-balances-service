from infrastructure.repository.base_repository import BaseRepository
from infrastructure.models import Snapshots, TransferInfo, StakingTokenSnapshot
from domain.factory.token_snapshot_factory import TokenSnapshotFactory
from sqlalchemy import exc


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
            raise (e)

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
            raise (e)

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
            raise (e)

        return result or None
