from sqlalchemy import BIGINT, VARCHAR, Column, TEXT, INT, text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.sql import func

Base = declarative_base()


class AuditClass(object):
    id = Column("row_id", BIGINT, primary_key=True, autoincrement=True)
    row_created = Column(
        "row_created",
        TIMESTAMP(),
        server_default=func.current_timestamp(),
        nullable=False,
    )
    row_updated = Column(
        "row_updated",
        TIMESTAMP(),
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        nullable=False,
    )


class Snapshots(AuditClass, Base):
    __tablename__ = "token_snapshots"
    address = Column("wallet_address", VARCHAR(50), nullable=False, index=True)
    block_number = Column("block_number", BIGINT, nullable=False)
    balance_in_cogs = Column("balance_in_cogs", BIGINT, nullable=False)
    snapshot_date = Column("snapshot_date", TIMESTAMP(), nullable=False)
    address_type = Column("address_type", INT, default=1)
    UniqueConstraint(address, name="uq_sn")


class UserAccessDetails(AuditClass, Base):
    __tablename__ = "user_access_details"
    wallet_address = Column("wallet_address", VARCHAR(50), nullable=False, index=True)
    email = Column("email", VARCHAR(120), nullable=False)
    name = Column("name", VARCHAR(60), nullable=True)
    login_time = Column("login_time", TIMESTAMP(), nullable=False)


class UserComments(AuditClass, Base):
    __tablename__ = "user_comments"
    wallet_address = Column("wallet_address", VARCHAR(50), nullable=False, index=True)
    comment = Column("comment", TEXT, nullable=False)


class TransferInfo(AuditClass, Base):
    __tablename__ = "transfer_info"
    wallet_address = Column("wallet_address", VARCHAR(50), nullable=False, index=True)
    transfer_time = Column("transfer_time", TIMESTAMP(), nullable=False)
    transfer_fees = Column("transfer_fees", BIGINT, nullable=False)
    transfer_transaction = Column("transfer_transaction", VARCHAR(255), nullable=False)
    transfer_amount_in_cogs = Column("transfer_amount_in_cogs", BIGINT, nullable=False)
    transfer_status = Column("transfer_status", VARCHAR(50), nullable=False)
    address_type = Column("address_type", INT, nullable=False)
