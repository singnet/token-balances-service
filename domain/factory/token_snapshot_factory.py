from datetime import date
from decimal import Decimal

from domain.models.cardano_balance import CardanoBalance
from domain.models.snapshot_history import SnapshotHistory
from domain.models.token import Token
from domain.models.token_snapshot import TokenSnapshot


class TokenSnapshotFactory:

    @staticmethod
    def convert_token_snapshot_db_to_entity_model(address, balance_in_cogs, block_number, snapshot_date):
        return TokenSnapshot(
            address,
            balance_in_cogs,
            block_number,
            snapshot_date
        )

    @staticmethod
    def token(row_id: int, id: str, name: str, blockchain_name: str, description: str, symbol: str,
              token_address: str, balance_types: str, allowed_decimal: int, is_enabled: bool, created_by: str,
              created_at: date, updated_at: date):
        return Token(row_id=row_id, id=id, name=name, blockchain_name=blockchain_name, description=description,
                     symbol=symbol, token_address=token_address, balance_types=balance_types,
                     allowed_decimal=allowed_decimal, is_enabled=is_enabled,
                     created_by=created_by, created_at=created_at, updated_at=updated_at)

    @staticmethod
    def snapshot_history(row_id: int, id: str, token_id: int, status: str, address_count: int, delta_count: int,
                         snapshot_date: date, snapshot_type: str, created_by: str, created_at: date, updated_at: date):
        return SnapshotHistory(row_id=row_id, id=id, token_id=token_id, status=status, address_count=address_count,
                               delta_count=delta_count, snapshot_date=snapshot_date, snapshot_type=snapshot_type,
                               created_by=created_by, created_at=created_at, updated_at=updated_at)

    @staticmethod
    def cardano_balance(row_id: int, id: str, token_id: int, address: str, stake_key: str, balance: Decimal,
                        balance_type: str, created_by: str, created_at: date, updated_at: date):
        return CardanoBalance(row_id=row_id, id=id, token_id=token_id, address=address, stake_key=stake_key,
                              balance=balance, balance_type=balance_type, created_by=created_by, created_at=created_at,
                              updated_at=updated_at)
