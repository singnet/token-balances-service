import json
from time import sleep
from unittest import TestCase
from http import HTTPStatus
from unittest.mock import patch

import application.services.cardano_db_sync_service
import utils.api
from application.handlers.balance_handler import get_token_balance, update_token_balance
from infrastructure.models import SnapshotHistoryDBModel, CardanoBalanceDBModel, TokenDBModel
from infrastructure.repository.token_snapshot_repo import TokenSnapshotRepo
from testcases.functionaltestcases.test_variables import TestVariables

token_repo = TokenSnapshotRepo()


class TestBalanceHandler(TestCase):

    def setUp(self):
        self.tearDown()

    def test_get_token_balance_with_empty_body(self):
        response = get_token_balance(event={"body": None}, context=None)
        self.assert_(response['statusCode'] == HTTPStatus.BAD_REQUEST.value)

    def test_get_token_balance_with_invalid_body(self):
        response = get_token_balance(event={"body": '{"email": "mail@mail.com"}'}, context=None)
        self.assert_(response['statusCode'] == HTTPStatus.BAD_REQUEST.value)

    def test_get_token_balance_with_valid_body(self):
        response = get_token_balance(event={"body": '{"wallet_address": "0x12345"}'}, context=None)
        self.assert_(response['statusCode'] == HTTPStatus.BAD_REQUEST.value)

    @patch("application.services.cardano_db_sync_service.CardanoDBSyncService.get_asset_holders")
    @patch("common.utils.Utils.report_slack")
    def test_update_token_balance(self, mock_report_slack, mock_get_asset_holders):
        success_request_no_tokens_available = {'status': 'success',
                                               'data': {'result': 'No tokens configured in the database'},
                                               'error': {'code': None, 'message': None, 'details': None}}
        success_request_tokens_available = {'status': 'success',
                                            'data': {'result': 'Successfully updated the token balance'},
                                            'error': {'code': None, 'message': None, 'details': None}}
        event = dict()
        # when token details are  not seeded in the database
        response = update_token_balance(event, {})
        body = json.loads(response["body"])
        self.assertEqual(body, success_request_no_tokens_available)

        # Adding token but not enabling for token balance update
        token_repo.session.add(TestVariables().token1)
        token_repo.session.commit()

        # when token details are  seeded in the database but not enabled for token balance update
        response = update_token_balance(event, {})
        body = json.loads(response["body"])
        self.assertEqual(body, success_request_no_tokens_available)

        # Adding token with enabling for token balance update
        token_repo.session.add(TestVariables().token2)
        token_repo.session.commit()

        mock_get_asset_holders.return_value = {
            "status": "success",
            "data": {
                "items": [
                    {
                        "address": "addr_test1qp4uans6u5l7cjn43my2xde2f8w80zcynw6q3sdzhf0fh67g0d53nsdsuwgcjl607j5tv5phzj7q93ad5rll20j8fjasfthpnc",
                        "stake_key": "stake_test1ury8k6gecxcw8yvf0a8lf29k2qm3f0qzc7k6pll48er5ewcvq465y",
                        "quantity": 7005199999974
                    },
                    {
                        "address": "addr_test1qqdchhslhycqpdjryevnyxxrtd7hx9pg29pzsnwm34f9ue03wly6jdq4lqw2w0d6zu8d3eltv0cuqm52lmxa2e5l7f8sy4nkgl",
                        "stake_key": "stake_test1urch0jdfxs2ls8988kapwrkcul4k8uwqd690anw4v60lyncs9ads5",
                        "quantity": 1781261462443
                    }
                ],
                "meta": {
                    "count": 2,
                    "policy_id": "6f1a1f0c7ccf632cc9ff4b79687ed13ffe5b624cce288b364ebdce50",
                    "asset_id": "41474958",
                    "asset_name": "AGIX"
                }
            },
            "error": {
                "code": None,
                "message": None,
                "details": None
            }
        }
        # when token details are  seeded in the database with enabling for token balance update
        response = update_token_balance(event, {})
        body = json.loads(response["body"])
        self.assertEqual(body, success_request_tokens_available)

        # snapshot history should be created with finished status
        snapshot_history = token_repo.session.query(SnapshotHistoryDBModel).all()

        self.assertEqual(len(snapshot_history), 1)
        self.assertEqual(snapshot_history[0].delta_count, 2)
        self.assertEqual(snapshot_history[0].address_count, 2)

        # Sleeping for 1 second, because assume after 2 seconds we are running the cron job
        sleep(1)

        # Running the snapshot but there is no change token balance from previous to current
        response = update_token_balance(event, {})
        body = json.loads(response["body"])
        self.assertEqual(body, success_request_tokens_available)

        # snapshot history should be created with finished status
        snapshot_history = token_repo.session.query(SnapshotHistoryDBModel).all()

        self.assertEqual(len(snapshot_history), 2)
        self.assertEqual(snapshot_history[1].delta_count, 0)
        self.assertEqual(snapshot_history[1].address_count, 2)

        # Sleeping for 1 second, because assume after 2 seconds we are running the cron job
        sleep(1)

        # Assume there is a change happened in one address balance
        mock_get_asset_holders.return_value = {
            "status": "success",
            "data": {
                "items": [
                    {
                        "address": "addr_test1qp4uans6u5l7cjn43my2xde2f8w80zcynw6q3sdzhf0fh67g0d53nsdsuwgcjl607j5tv5phzj7q93ad5rll20j8fjasfthpnc",
                        "stake_key": "stake_test1ury8k6gecxcw8yvf0a8lf29k2qm3f0qzc7k6pll48er5ewcvq465y",
                        "quantity": 7005199999975
                    },
                    {
                        "address": "addr_test1qqdchhslhycqpdjryevnyxxrtd7hx9pg29pzsnwm34f9ue03wly6jdq4lqw2w0d6zu8d3eltv0cuqm52lmxa2e5l7f8sy4nkgl",
                        "stake_key": "stake_test1urch0jdfxs2ls8988kapwrkcul4k8uwqd690anw4v60lyncs9ads5",
                        "quantity": 1781261462443
                    }
                ],
                "meta": {
                    "count": 2,
                    "policy_id": "6f1a1f0c7ccf632cc9ff4b79687ed13ffe5b624cce288b364ebdce50",
                    "asset_id": "41474958",
                    "asset_name": "AGIX"
                }
            },
            "error": {
                "code": None,
                "message": None,
                "details": None
            }
        }

        # Running the snapshot but there is  change token balance from previous to current
        response = update_token_balance(event, {})
        body = json.loads(response["body"])
        self.assertEqual(body, success_request_tokens_available)

        # snapshot history should be created with finished status
        snapshot_history = token_repo.session.query(SnapshotHistoryDBModel).all()

        self.assertEqual(len(snapshot_history), 3)
        self.assertEqual(snapshot_history[2].delta_count, 2)
        self.assertEqual(snapshot_history[2].address_count, 2)

        # Sleeping for 1 second, because assume after 2 seconds we are running the cron job
        sleep(1)

        # Assume there is a change happened and only one address has balance
        mock_get_asset_holders.return_value = {
            "status": "success",
            "data": {
                "items": [
                    {
                        "address": "addr_test1qp4uans6u5l7cjn43my2xde2f8w80zcynw6q3sdzhf0fh67g0d53nsdsuwgcjl607j5tv5phzj7q93ad5rll20j8fjasfthpnc",
                        "stake_key": "stake_test1ury8k6gecxcw8yvf0a8lf29k2qm3f0qzc7k6pll48er5ewcvq465y",
                        "quantity": 7005199999975
                    }
                ],
                "meta": {
                    "count": 1,
                    "policy_id": "6f1a1f0c7ccf632cc9ff4b79687ed13ffe5b624cce288b364ebdce50",
                    "asset_id": "41474958",
                    "asset_name": "AGIX"
                }
            },
            "error": {
                "code": None,
                "message": None,
                "details": None
            }
        }

        # Running the snapshot but there is  change token balance from previous to current
        response = update_token_balance(event, {})
        body = json.loads(response["body"])
        self.assertEqual(body, success_request_tokens_available)

        # snapshot history should be created with finished status
        snapshot_history = token_repo.session.query(SnapshotHistoryDBModel).all()

        self.assertEqual(len(snapshot_history), 4)
        self.assertEqual(snapshot_history[3].delta_count, 1)
        self.assertEqual(snapshot_history[3].address_count, 1)

    def tearDown(self):
        token_repo.session.query(SnapshotHistoryDBModel).delete()
        token_repo.session.query(CardanoBalanceDBModel).delete()
        token_repo.session.commit()
        token_repo.session.query(TokenDBModel).delete()
        token_repo.session.commit()
