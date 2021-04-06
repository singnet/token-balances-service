from sqlalchemy import BIGINT, DECIMAL, VARCHAR, Column, DateTime, Date, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class BaseClassMixin(object):
    id = Column("row_id", BIGINT, primary_key=True, autoincrement=True)
    row_created = Column("row_created", DateTime,
                         server_default=func.current_timestamp(), nullable=False)
    row_updated = Column("row_updated", DateTime,
                         server_default=func.current_timestamp(), server_onupdate=func.current_timestamp(), nullable=False)


class Snapshots(BaseClassMixin, Base):
    __tablename__ = "snapshots"
    address = Column("address", VARCHAR(50), nullable=False, index=True)
    block_number = Column("block_number", BIGINT, nullable=False)
    balance_in_cogs = Column("balance_in_cogs", DECIMAL(19, 8), nullable=False)
    snapshot_date = Column("snapshot_date", Date, nullable=False)


class UserAccessDetails(BaseClassMixin, Base):
    __tablename__ = "user_access_details"
    wallet_address = Column("wallet_address", VARCHAR(
        50), nullable=False, index=True)
    email = Column("email", VARCHAR(
        120), nullable=False)
    name = Column("name", VARCHAR(
        60), nullable=False)
    login_time = Column("login_time", DateTime, nullable=False)


class UserComments(BaseClassMixin, Base):
    __tablename__ = "user_comments"
    wallet_address = Column("wallet_address", VARCHAR(
        50), nullable=False, index=True)
    comment = Column("comment", TEXT, nullable=False)


class TransferInfo(BaseClassMixin, Base):
    __tablename__ = "transfer_info"
    wallet_address = Column("wallet_address", VARCHAR(
        50), nullable=False, index=True)
    transfer_time = Column("transfer_time", DateTime, nullable=False)

    transfer_fees = Column("transfer_fees", DECIMAL(19, 8), nullable=False)
    transfer_transaction = Column(
        "transfer_transaction", VARCHAR(50), nullable=False)
    transfer_amount_in_cogs = Column(
        "transfer_amount_in_cogs", DECIMAL(19, 8), nullable=False)
    transfer_status = Column(
        "transfer_status", VARCHAR(50), nullable=False)
