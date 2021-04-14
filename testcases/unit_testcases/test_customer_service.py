from http import HTTPStatus
from unittest import TestCase
from application.services.customer_service import submit_user_question


class TestCustomerService(TestCase):
    def test_submit_user_question(self):
        payload = {
            "wallet_address": "0x12345567",
            "email": "test@mail.com",
            "comment": "test comment",
            "name": "test name",
        }
        statusCode, message = submit_user_question(payload)
        assert statusCode == HTTPStatus.OK.value
