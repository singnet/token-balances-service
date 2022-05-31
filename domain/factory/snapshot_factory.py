from datetime import date

from domain.models.snapshot_history import SnapshotHistory
from domain.models.token import Token


class SnapshotFactory:

    @staticmethod
    def token(row_id: int, id: str, name: str, blockchain_name: str, description: str, symbol: str,
              token_address: str, allowed_decimal: int, is_enabled: bool, created_by: str, created_at: date,
              updated_at: date):
        return Token(row_id=row_id, id=id, name=name, blockchain_name=blockchain_name, description=description,
                     symbol=symbol,
                     token_address=token_address, allowed_decimal=allowed_decimal, is_enabled=is_enabled,
                     created_by=created_by, created_at=created_at,
                     updated_at=updated_at)

    @staticmethod
    def snapshot_history(row_id: int, id: str, token_id: int, status: str, address_count: int, snapshot_date: date,
                         snapshot_type: str, created_by: str, created_at: date, updated_at: date):
        return SnapshotHistory(row_id=row_id, id=id, token_id=token_id, status=status, address_count=address_count,
                               snapshot_date=snapshot_date, snapshot_type=snapshot_type, created_by=created_by,
                               created_at=created_at, updated_at=updated_at)
