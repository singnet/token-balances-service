from sqlalchemy import BIGINT, DECIMAL, VARCHAR, Column, DateTime, Date, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Snapshots(Base):
    __tablename__ = "snapshots"
    id = Column("id", BIGINT, primary_key=True, autoincrement=True)
    wallet_address = Column("wallet_address", VARCHAR(
        50), nullable=False, index=True)
    block_number = Column("block_number", BIGINT, nullable=False)
    amount_held_in_cogs = Column(
        "amount_held_in_cogs", DECIMAL(19, 8), nullable=False)
    snap_shot_date = Column("snap_shot_date", Date, nullable=False)
    created_at = Column("created_at", DateTime,
                        server_default=func.current_timestamp(), nullable=False)
    updated_at = Column("updated_at", DateTime,
                        server_default=func.current_timestamp(), server_onupdate=func.current_timestamp(), nullable=False)


class UserAccessDetails(Base):
    __tablename__ = "user_access_details"
    id = Column("id", BIGINT, primary_key=True, autoincrement=True)
    wallet_address = Column("wallet_address", VARCHAR(
        50), nullable=False, index=True)
    email = Column("email", VARCHAR(
        120), nullable=False)
    name = Column("name", VARCHAR(
        60), nullable=False)
    login_time = Column("login_time", DateTime, nullable=False)
    created_at = Column("created_at", DateTime,
                        server_default=func.current_timestamp(), nullable=False)
    updated_at = Column("updated_at", DateTime,
                        server_default=func.current_timestamp(), server_onupdate=func.current_timestamp(), nullable=False)


class UserComments(Base):
    __tablename__ = "user_comments"
    id = Column("id", BIGINT, primary_key=True, autoincrement=True)
    wallet_address = Column("wallet_address", VARCHAR(
        50), nullable=False, index=True)
    comment = Column("comment", TEXT, nullable=False)
    created_at = Column("created_at", DateTime,
                        server_default=func.current_timestamp(), nullable=False)
    updated_at = Column("updated_at", DateTime,
                        server_default=func.current_timestamp(), server_onupdate=func.current_timestamp(), nullable=False)


class TransferInfo(Base):
    __tablename__ = "transfer_info"
    id = Column("id", BIGINT, primary_key=True, autoincrement=True)
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

    created_at = Column("created_at", DateTime,
                        server_default=func.current_timestamp(), nullable=False)
    updated_at = Column("updated_at", DateTime,
                        server_default=func.current_timestamp(), server_onupdate=func.current_timestamp(), nullable=False)
