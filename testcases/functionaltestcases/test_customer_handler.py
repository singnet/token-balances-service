from unittest import TestCase
from http import HTTPStatus
from application.handlers.customer_handler import submit_question, register


class TestCustomerHandler(TestCase):
    def test_submit_question_with_empty_body(self):
        response = submit_question(event={"body": None, "headers": {}}, context=None)
        self.assert_(response['statusCode'] == HTTPStatus.BAD_REQUEST.value)

    def test_submit_question_with_valid_body(self):
        response = submit_question(event={"body": '{"email": "mail@mail.com"}', "headers": {
            "Authorization": "0x36980e7e7ccfe437a5b60ccf26221b2b9ff6f80f39548162d7764c7e7a0992256c42670244b21f5d367420c656aef86e9a164944f10d4f6e64d303c8b575a0d71b"}},
                                   context=None)
        self.assert_(response['statusCode'] == HTTPStatus.BAD_REQUEST.value)

    def test_submit_question_with_invalid_body(self):
        response = submit_question(
            event={"body": '{"wallet_address": "0x12345", "comment": "test comment", "email": "mail@mail.com"}',
                   "headers": {}}, context=None)
        self.assert_(response['statusCode'] == HTTPStatus.BAD_REQUEST.value)

    def test_submit_question_with_block_number_as_string(self):
        response = submit_question(event={
            "body": '{"wallet_address": "0x176133a958449C28930970989dB5fFFbEdd9F447","email": "user@mail.com","comment": "hello world","block_number": "12333949"}',
            "headers": {
                "Authorization": "0x36980e7e7ccfe437a5b60ccf26221b2b9ff6f80f39548162d7764c7e7a0992256c42670244b21f5d367420c656aef86e9a164944f10d4f6e64d303c8b575a0d71b"}},
            context=None)
        self.assertTrue(response['statusCode'] == HTTPStatus.BAD_REQUEST.value)

    def test_submit_question_with_block_number_as_number(self):
        response = submit_question(event={
            "body": '{"wallet_address": "0x176133a958449C28930970989dB5fFFbEdd9F447","email": "user@mail.com","comment": "hello world","block_number": 12333949}',
            "headers": {
                "Authorization": "0x36980e7e7ccfe437a5b60ccf26221b2b9ff6f80f39548162d7764c7e7a0992256c42670244b21f5d367420c656aef86e9a164944f10d4f6e64d303c8b575a0d71b"}},
            context=None)
        self.assertTrue(response['statusCode'] == HTTPStatus.OK.value)

    def test_create_user_with_invalid_request(self):
        response = register(
            event={"body": '{"wallet_address": "0x12345", "block_number": "0x12345", "email": "mail@mail.com"}',
                   "headers": {}}, context=None)
        self.assert_(response['statusCode'] == HTTPStatus.BAD_REQUEST.value)

    def test_create_user_with_request(self):
        response = register(
            event={"body": '{"wallet_address": "0x12345", "block_number": "0x12345", "email": "mail@mail.com"}',
                   "headers": {
                       "Authorization": "0x36980e7e7ccfe437a5b60ccf26221b2b9ff6f80f39548162d7764c7e7a0992256c42670244b21f5d367420c656aef86e9a164944f10d4f6e64d303c8b575a0d71b"}},
            context=None)
        self.assert_(response['statusCode'] == HTTPStatus.BAD_REQUEST.value)
