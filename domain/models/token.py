from datetime import date

from constants.entity import TokenEntities
from utils.general import datetime_to_str


class Token:

    def __init__(self, row_id: int, id: str, name: str, blockchain_name: str, description: str, symbol: str,
                 token_address: str, balance_types: str, allowed_decimal: int, is_enabled: bool, created_by: str,
                 created_at: date, updated_at: date):
        self.row_id = row_id
        self.id = id
        self.name = name
        self.blockchain_name = blockchain_name
        self.description = description
        self.symbol = symbol
        self.token_address = token_address
        self.balance_types = [balance_type.strip() for balance_type in balance_types.split(',')]
        self.allowed_decimal = allowed_decimal
        self.is_enabled = is_enabled
        self.created_by = created_by
        self.created_at = datetime_to_str(created_at)
        self.updated_at = datetime_to_str(updated_at)

    def to_dict(self):
        return {
            TokenEntities.ROW_ID.value: self.row_id,
            TokenEntities.ID.value: self.id,
            TokenEntities.NAME.value: self.name,
            TokenEntities.BLOCKCHAIN_NAME.value: self.blockchain_name,
            TokenEntities.DESCRIPTION.value: self.description,
            TokenEntities.SYMBOL.value: self.symbol,
            TokenEntities.TOKEN_ADDRESS.value: self.token_address,
            TokenEntities.BALANCE_TYPES.value: self.balance_types,
            TokenEntities.ALLOWED_DECIMAL.value: self.allowed_decimal,
            TokenEntities.IS_ENABLED.value: self.is_enabled,
            TokenEntities.CREATED_BY.value: self.created_by,
            TokenEntities.CREATED_AT.value: self.created_at,
            TokenEntities.UPDATED_AT.value: self.updated_at,
        }
