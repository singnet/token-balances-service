from unittest import TestCase
from http import HTTPStatus
from application.handlers.customer_handler import submit_question


class TestCustomerHandler(TestCase):
    def test_submit_question_with_empty_body(self):
        response = submit_question(event={"body": None}, context=None)
        self.assert_(response['statusCode'] == HTTPStatus.BAD_REQUEST.value)

    def test_submit_question_with_invalid_body(self):
        response = submit_question(event={"body": '{"email": "mail@mail.com"}'}, context=None)
        self.assert_(response['statusCode'] == HTTPStatus.BAD_REQUEST.value)

    def test_submit_question_with_valid_body(self):
        response = submit_question(event={"body": '{"wallet_address": "0x12345", "comment": "test comment", "email": "mail@mail.com"}'}, context=None)
        self.assert_(response['statusCode'] == HTTPStatus.OK.value)
