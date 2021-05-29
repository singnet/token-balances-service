class TokenSnapshot:
    def __init__(
        self, address, balance_in_cogs, block_no, snapshot_date, token_transfer_details, staker_transfer_details
    ):
        self.address = address
        self.balance_in_cogs = balance_in_cogs
        self.block_no = block_no
        self.snapshot_date = snapshot_date
        self.token_transfer_details = token_transfer_details
        self.staker_transfer_details = staker_transfer_details

    def to_response(self):
        token_snapshot = {
            "wallet_address": self.address,
            "balance_in_cogs": self.balance_in_cogs,
            "snapshot_date": str(self.snapshot_date),
            "block_no": self.block_no,
            "token_transfer_details": None,
            "staker_transfer_details": None
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
                "comment": self.staker_transfer_details.comment
            }

        return token_snapshot
