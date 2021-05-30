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
