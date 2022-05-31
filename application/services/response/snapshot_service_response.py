from constants.entity import TokenEntities, SnapshotHistoryEntities


def get_available_tokens_response_format(tokens):
    return [{
        TokenEntities.ROW_ID.value: token.get(TokenEntities.ROW_ID.value),
        TokenEntities.ID.value: token.get(TokenEntities.ID.value),
        TokenEntities.NAME.value: token.get(TokenEntities.NAME.value),
        TokenEntities.BLOCKCHAIN_NAME.value: token.get(TokenEntities.BLOCKCHAIN_NAME.value),
        TokenEntities.DESCRIPTION.value: token.get(TokenEntities.DESCRIPTION.value),
        TokenEntities.SYMBOL.value: token.get(TokenEntities.SYMBOL.value),
        TokenEntities.TOKEN_ADDRESS.value: token.get(TokenEntities.TOKEN_ADDRESS.value),
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
