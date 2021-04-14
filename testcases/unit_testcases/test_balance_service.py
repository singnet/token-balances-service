from http import HTTPStatus
from unittest import TestCase
from application.services.balance_service import get_snapshot_by_address


class TestBalanceService(TestCase):
    def test_get_snapshot_by_address(self):
        address = "0x12345567"
        statusCode, message, data = get_snapshot_by_address(address)
        assert statusCode == HTTPStatus.BAD_REQUEST.value
