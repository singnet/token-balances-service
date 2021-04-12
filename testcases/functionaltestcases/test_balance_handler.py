from unittest import TestCase
from http import HTTPStatus
from application.handlers.balance_handler import get_token_balance


class TestBalanceHandler(TestCase):
    def test_get_token_balance_with_empty_body(self):
        response = get_token_balance(event={"body": None}, context=None)
        self.assert_(response['statusCode'] == HTTPStatus.BAD_REQUEST.value)

    def test_get_token_balance_with_invalid_body(self):
        response = get_token_balance(event={"body": '{"email": "mail@mail.com"}'}, context=None)
        self.assert_(response['statusCode'] == HTTPStatus.BAD_REQUEST.value)

    def test_get_token_balance_with_valid_body(self):
        response = get_token_balance(event={"body": '{"wallet_address": "0x12345"}'}, context=None)
        self.assert_(response['statusCode'] == HTTPStatus.BAD_REQUEST.value)
