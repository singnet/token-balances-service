from datetime import date

from constants.entity import SnapshotHistoryEntities
from utils.general import datetime_to_str


class SnapshotHistory:

    def __init__(self, row_id: int, id: str, token_id: int, status: str, address_count: int, delta_count:int,  snapshot_date: date,
                 snapshot_type: str, created_by: str, created_at: date, updated_at: date):
        self.row_id = row_id
        self.id = id
        self.token_id = token_id
        self.status = status
        self.address_count = address_count
        self.delta_count = delta_count
        self.snapshot_date = snapshot_date
        self.snapshot_type = snapshot_type
        self.created_by = created_by
        self.created_at = datetime_to_str(created_at)
        self.updated_at = datetime_to_str(updated_at)

    def to_dict(self):
        return {
            SnapshotHistoryEntities.ROW_ID.value: self.row_id,
            SnapshotHistoryEntities.ID.value: self.id,
            SnapshotHistoryEntities.TOKEN_ID.value: self.token_id,
            SnapshotHistoryEntities.STATUS.value: self.status,
            SnapshotHistoryEntities.ADDRESS_COUNT.value: self.address_count,
            SnapshotHistoryEntities.DELTA_COUNT.value: self.delta_count,
            SnapshotHistoryEntities.SNAPSHOT_DATE.value: self.snapshot_date,
            SnapshotHistoryEntities.SNAPSHOT_TYPE.value: self.snapshot_type,
            SnapshotHistoryEntities.CREATED_BY.value: self.created_by,
            SnapshotHistoryEntities.CREATED_AT.value: self.created_at,
            SnapshotHistoryEntities.UPDATED_AT.value: self.updated_at
        }
