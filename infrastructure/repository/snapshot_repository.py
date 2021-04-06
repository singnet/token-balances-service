from infrastructure.repository.base_repository import BaseRepository
from infrastructure.models import Snapshots, TransferInfo


class Snapshot(BaseRepository):
    def find_by_address(self, address):

        result = (
            self.session.query(Snapshots)
            .filter(Snapshots.address == address)
            .limit(1)
            .first()
        )

        return result or None

    def find_transfer_status(self, address):
        result = (
            self.session.query(TransferInfo)
            .filter(TransferInfo.wallet_address == address)
            .limit(1)
            .first()
        )

        return result or None
