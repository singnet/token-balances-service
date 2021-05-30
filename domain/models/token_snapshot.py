class TokenSnapshot:
    def __init__(
            self,
            snapshot_details,
            token_transfer_details,
            staker_transfer_details,
    ):
        self.snapshot_details = snapshot_details
        self.token_transfer_details = token_transfer_details
        self.staker_transfer_details = staker_transfer_details

    def to_response(self):
        token_snapshot = {}

        if self.snapshot_details is not None:
            token_snapshot = {
                "wallet_address": self.snapshot_details.address,
                "balance_in_cogs": self.snapshot_details.balance_in_cogs,
                "snapshot_date": str(self.snapshot_details.snapshot_date),
                "block_no": self.snapshot_details.block_number or None,
                "token_transfer_details": None,
                "staker_transfer_details": None,
            }

        if self.token_transfer_details is not None:
            token_snapshot["token_transfer_details"] = {
                "converted_tokens": self.token_transfer_details.transfer_amount_in_cogs,
                "transfer_time": str(self.token_transfer_details.transfer_time),
                "transaction_hash": self.token_transfer_details.transfer_transaction,
            }

        if self.staker_transfer_details is not None:
            token_snapshot["staker_transfer_details"] = {
                "converted_tokens": self.staker_transfer_details.balance_in_cogs,
                "staker_address": self.staker_transfer_details.staker_address,
                "comment": self.staker_transfer_details.comment,
            }

        return token_snapshot
