from datetime import date
from decimal import Decimal

from constants.entity import CardanoBalanceEntities
from utils.general import datetime_to_str


class CardanoBalance:

    def __init__(self, row_id: int, id: str, token_id: int, address: str, stake_key: str, balance: Decimal,
                 balance_type: str, created_by: str, created_at: date, updated_at: date):
        self.row_id = row_id
        self.id = id
        self.token_id = token_id
        self.address = address
        self.stake_key = stake_key
        self.balance = int(balance)
        self.balance_type = balance_type
        self.created_by = created_by
        self.created_at = datetime_to_str(created_at)
        self.updated_at = datetime_to_str(updated_at)

    def to_dict(self):
        return {
            CardanoBalanceEntities.ROW_ID.value: self.row_id,
            CardanoBalanceEntities.ID.value: self.id,
            CardanoBalanceEntities.TOKEN_ID.value: self.token_id,
            CardanoBalanceEntities.ADDRESS.value: self.address,
            CardanoBalanceEntities.STAKE_KEY.value: self.stake_key,
            CardanoBalanceEntities.BALANCE.value: self.balance,
            CardanoBalanceEntities.BALANCE_TYPE.value: self.balance_type,
            CardanoBalanceEntities.CREATED_BY.value: self.created_by,
            CardanoBalanceEntities.CREATED_AT.value: self.created_at,
            CardanoBalanceEntities.UPDATED_AT.value: self.updated_at

        }
