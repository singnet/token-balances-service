from domain.models.token_snapshot import TokenSnapshot


class TokenSnapshotFactory:
    def convert_token_snapshot_db_to_entity_model(snapshot, token_transfer_details, staker_transfer_details):
        return TokenSnapshot(
            snapshot,
            token_transfer_details,
            staker_transfer_details
        )
