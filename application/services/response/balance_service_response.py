from constants.entity import TokenEntities, SnapshotHistoryEntities, CardanoBalanceEntities, \
    CardanoDBSyncApiResponseEntities, UpdateTokenBalanceEntity


def get_available_tokens_response_format(tokens: list):
    return [{
        TokenEntities.ROW_ID.value: token.get(TokenEntities.ROW_ID.value),
        TokenEntities.ID.value: token.get(TokenEntities.ID.value),
        TokenEntities.NAME.value: token.get(TokenEntities.NAME.value),
        TokenEntities.BLOCKCHAIN_NAME.value: token.get(TokenEntities.BLOCKCHAIN_NAME.value),
        TokenEntities.DESCRIPTION.value: token.get(TokenEntities.DESCRIPTION.value),
        TokenEntities.SYMBOL.value: token.get(TokenEntities.SYMBOL.value),
        TokenEntities.TOKEN_ADDRESS.value: token.get(TokenEntities.TOKEN_ADDRESS.value),
        TokenEntities.BALANCE_TYPES.value: token.get(TokenEntities.BALANCE_TYPES.value),
        TokenEntities.ALLOWED_DECIMAL.value: token.get(TokenEntities.ALLOWED_DECIMAL.value),
        TokenEntities.IS_ENABLED.value: token.get(TokenEntities.IS_ENABLED.value),
        TokenEntities.CREATED_BY.value: token.get(TokenEntities.CREATED_BY.value),
        TokenEntities.CREATED_AT.value: token.get(TokenEntities.CREATED_AT.value),
        TokenEntities.UPDATED_AT.value: token.get(TokenEntities.UPDATED_AT.value),
    } for token in tokens]


def create_snapshot_history_response_format(snapshot_history):
    return {
        SnapshotHistoryEntities.ROW_ID.value: snapshot_history.get(SnapshotHistoryEntities.ROW_ID.value),
        SnapshotHistoryEntities.ID.value: snapshot_history.get(SnapshotHistoryEntities.ID.value),
        SnapshotHistoryEntities.TOKEN_ID.value: snapshot_history.get(SnapshotHistoryEntities.TOKEN_ID.value),
        SnapshotHistoryEntities.STATUS.value: snapshot_history.get(SnapshotHistoryEntities.STATUS.value),
        SnapshotHistoryEntities.ADDRESS_COUNT.value: snapshot_history.get(SnapshotHistoryEntities.ADDRESS_COUNT.value),
        SnapshotHistoryEntities.SNAPSHOT_DATE.value: snapshot_history.get(SnapshotHistoryEntities.SNAPSHOT_DATE.value),
        SnapshotHistoryEntities.SNAPSHOT_TYPE.value: snapshot_history.get(SnapshotHistoryEntities.SNAPSHOT_TYPE.value),
        SnapshotHistoryEntities.CREATED_BY.value: snapshot_history.get(SnapshotHistoryEntities.CREATED_BY.value),
        SnapshotHistoryEntities.CREATED_AT.value: snapshot_history.get(SnapshotHistoryEntities.CREATED_AT.value),
        SnapshotHistoryEntities.UPDATED_AT.value: snapshot_history.get(SnapshotHistoryEntities.UPDATED_AT.value)
    }


def get_token_holders_response_format(token_holders: list):
    return [{
        CardanoBalanceEntities.ROW_ID.value: token_holder.get(CardanoBalanceEntities.ROW_ID.value),
        CardanoBalanceEntities.ID.value: token_holder.get(CardanoBalanceEntities.ID.value),
        CardanoBalanceEntities.TOKEN_ID.value: token_holder.get(CardanoBalanceEntities.TOKEN_ID.value),
        CardanoBalanceEntities.ADDRESS.value: token_holder.get(CardanoBalanceEntities.ADDRESS.value),
        CardanoBalanceEntities.STAKE_KEY.value: token_holder.get(CardanoBalanceEntities.STAKE_KEY.value),
        CardanoBalanceEntities.BALANCE.value: token_holder.get(CardanoBalanceEntities.BALANCE.value),
        CardanoBalanceEntities.BALANCE_TYPE.value: token_holder.get(CardanoBalanceEntities.BALANCE_TYPE.value),
        CardanoBalanceEntities.CREATED_BY.value: token_holder.get(CardanoBalanceEntities.CREATED_BY.value),
        CardanoBalanceEntities.CREATED_AT.value: token_holder.get(CardanoBalanceEntities.CREATED_AT.value),
        CardanoBalanceEntities.UPDATED_AT.value: token_holder.get(CardanoBalanceEntities.UPDATED_AT.value)
    } for token_holder in token_holders]


def existing_token_holders_response_format(existing_token_holders):
    return [{
        CardanoBalanceEntities.ADDRESS.value: existing_token_holder.get(CardanoBalanceEntities.ADDRESS.value),
        CardanoBalanceEntities.STAKE_KEY.value: existing_token_holder.get(CardanoBalanceEntities.STAKE_KEY.value),
        CardanoDBSyncApiResponseEntities.QUANTITY.value: existing_token_holder.get(CardanoBalanceEntities.BALANCE.value)
    } for existing_token_holder in existing_token_holders]


def process_update_token_balance_response_format(delta_count: int, insert_count: int, delete_count: int,
                                                 current_count: int):
    return {
        UpdateTokenBalanceEntity.DELTA_COUNT.value: delta_count,
        UpdateTokenBalanceEntity.INSERT_COUNT.value: insert_count,
        UpdateTokenBalanceEntity.DELETE_COUNT.value: delete_count,
        UpdateTokenBalanceEntity.CURRENT_COUNT.value: current_count,
    }


def update_token_balance_response_format(result):
    return {
        "result": result
    }
