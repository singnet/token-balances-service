from infrastructure.models import TokenDBModel


def create_token(id, name, blockchain_name, description, symbol, token_address, balance_types, allowed_decimal,
                 is_enabled, created_by, created_at, updated_at):
    return TokenDBModel(id=id, name=name, blockchain_name=blockchain_name, description=description, symbol=symbol,
                        token_address=token_address, balance_types=balance_types, allowed_decimal=allowed_decimal,
                        is_enabled=is_enabled, created_by=created_by, created_at=created_at, updated_at=updated_at)


class TestVariables:

    def __init__(self):
        created_at = "2022-06-01 04:10:54"
        updated_at = "2022-06-01 04:10:54"

        self.token_id_1 = "5aab34c9eea4469ea0d186d2a5f19395"
        self.token_id_2 = "1a6769723f6a44f2b8b15c85902b4601"
        self.token_id_3 = "5d6bb03d76c64fdf96bef2324d37406d"

        self.token1 = create_token(id=self.token_id_1, name="SNET AGIX", blockchain_name="ethereum",
                                   description="Singularity net agix on ethereum", symbol="AGIX",
                                   token_address="0xa1e841e8f770e5c9507e2f8cfd0aa6f73009715d",
                                   balance_types="token", allowed_decimal=8, is_enabled=False, created_by="TestCase",
                                   created_at=created_at, updated_at=updated_at)
        self.token2 = create_token(id=self.token_id_2, name="SNET AGIX", blockchain_name="cardano",
                                   description="Singularity net agix on cardano", symbol="AGIX",
                                   token_address="6f1a1f0c7ccf632cc9ff4b79687ed13ffe5b624cce288b364ebdce50",
                                   balance_types="token", allowed_decimal=8, is_enabled=True, created_by="TestCase",
                                   created_at=created_at, updated_at=updated_at)
        self.token3 = create_token(id=self.token_id_3, name="Nunet NTX", blockchain_name="cardano",
                                   description="Nunet token on cardano", symbol="NTX",
                                   token_address="b5094f93ff9fcba9e8b257197d589cbcde3d92a108804e3a378bd2ce",
                                   balance_types="token", allowed_decimal=6, is_enabled=True, created_by="TestCase",
                                   created_at=created_at, updated_at=updated_at)
