from sqlalchemy import BIGINT, DATE, DECIMAL, VARCHAR, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Snapshots(Base):
    __tablename__ = "snapshots"
    id = Column("id", BIGINT, primary_key=True, autoincrement=True)
    wallet_address = Column("wallet_address", VARCHAR(
        50), nullable=False, index=True)
    block_number = Column("block_number", BIGINT, nullable=False)
    amount_held_in_cogs = Column(
        "amount_held_in_cogs", DECIMAL(19, 8), nullable=False)
    snap_shot_date = Column("snap_shot_date", DATE,
                            server_default=db.func.now())
    created_at = Column("created_at", DateTime, server_default=db.func.now())
    updated_at = Column("updated_at", DateTime,
                        server_default=db.func.now(), server_onupdate=db.func.now())
