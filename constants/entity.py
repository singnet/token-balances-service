from enum import Enum


class TokenEntities(Enum):
    ROW_ID = "row_id"
    ID = "id"
    NAME = "name"
    BLOCKCHAIN_NAME = "blockchain_name"
    DESCRIPTION = "description"
    SYMBOL = "symbol"
    TOKEN_ADDRESS = "token_address"
    ALLOWED_DECIMAL = "allowed_decimal"
    IS_ENABLED = "is_enabled"
    CREATED_BY = "created_by"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class SnapshotHistoryEntities(Enum):
    ROW_ID = "row_id"
    ID = "id"
    TOKEN_ID = "token_id"
    STATUS = "status"
    ADDRESS_COUNT = "address_count"
    SNAPSHOT_DATE = "snapshot_date"
    SNAPSHOT_TYPE = "snapshot_type"
    CREATED_BY = "created_by"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class CardanoDBSyncApiResponseEntities(Enum):
    STATUS = "status"
    DATA = "data"
    ITEMS = "items"
    ADDRESS = "address"
    STAKE_KEY = "stake_key"
    BALANCE = "balance"
    META = "meta"
    COUNT = "meta"


class APIStatusResponse(Enum):
    SUCCESS = "success"
    FAILED = "failed"
