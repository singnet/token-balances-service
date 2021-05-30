class TokenSnapshot:
    def __init__(
            self, address, balance_in_cogs, block_no, snapshot_date):
        self.address = address
        self.balance_in_cogs = balance_in_cogs
        self.block_no = block_no
        self.snapshot_date = snapshot_date
        self.__token_transfer_details = {
            "converted_tokens": 0,
            "transfer_time": "",
            "transaction_hash": "",
        }
        self.__staker_transfer_details = {
            "converted_tokens": 0,
            "staker_address": "",
            "comment": ""
        }

    @property
    def token_transfer_details(self):
        return self.__token_transfer_details

    @token_transfer_details.setter
    def token_transfer_details(self, tranfer_details):
        if tranfer_details is not None:
            self.__token_transfer_details = {
                "converted_tokens": tranfer_details.transfer_amount_in_cogs,
                "transfer_time": str(tranfer_details.transfer_time),
                "transaction_hash": tranfer_details.transfer_transaction,
            }

    @property
    def staker_transfer_details(self):
        return self.__staker_transfer_details

    @staker_transfer_details.setter
    def staker_transfer_details(self, staker_details):
        if staker_details is not None:
            self.__staker_transfer_details = {
                "converted_tokens": staker_details.balance_in_cogs,
                "staker_address": staker_details.staker_address,
                "comment": staker_details.comment
            }

    def to_response(self):
        token_snapshot = {
            "wallet_address": self.address,
            "balance_in_cogs": self.balance_in_cogs,
            "snapshot_date": str(self.snapshot_date),
            "block_no": self.block_no,
            "token_transfer_details": self.__token_transfer_details,
            "staker_transfer_details": self.__staker_transfer_details
        }

        return token_snapshot
