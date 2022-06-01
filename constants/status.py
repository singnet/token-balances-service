from enum import Enum


class SnapshotHistoryStatus(Enum):
    STARTED = "started"
    FINISHED = "finished"
    FAILED = "failed"


class SnapshotType(Enum):
    TOKEN = "token"
    ADA = "ada"
    STAKING = "staking"


class CreatedBy(Enum):
    BACKEND = "backend"


class ApiMethodType(Enum):
    GET = "get"
    POST = "post"
