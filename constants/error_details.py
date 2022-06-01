from enum import Enum


class ErrorCode(Enum):
    MISSING_BODY = "E0001"
    EMPTY_SCHEMA_FILE = "E0002"
    SCHEMA_NOT_MATCHING = "E0003"
    UNEXPECTED_ERROR_SCHEMA_VALIDATION = "E0004"
    PROPERTY_VALUES_EMPTY = "E0005"
    UNEXPECTED_ERROR_ON_CARDANO_DB_SYNC_SERVICE_CALL = "E0006"
    UNEXPECTED_API_METHOD_PROVIDED = "E0007"
    API_FAILED = "E008"


class ErrorDetails(Enum):
    E0001 = "Missing body"
    E0002 = "Schema is Empty"
    E0003 = "Schema is not matching with request"
    E0004 = "Unexpected error occurred during schema validation"
    E0005 = "Property value is empty"
    E0006 = "Unexpected error occurred while calling the cardano db sync service"
    E0007 = "Unexpected api method type provided"
    E008 = "Api call failed"
