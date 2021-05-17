import web3

from eth_account.messages import defunct_hash_message, encode_defunct
from infrastructure.repository.customer_comments_repo import CustomerComments
from infrastructure.repository.user_repository import UserRepository
from http import HTTPStatus
from web3 import Web3
from config import HTTP_PROVIDER, BLOCK_THRESHOLD

web3_object = Web3(web3.providers.HTTPProvider(HTTP_PROVIDER))


def register_user(payload, signature):
    statusCode = HTTPStatus.BAD_REQUEST.value
    message = HTTPStatus.BAD_REQUEST.phrase

    wallet_address = payload["wallet_address"]
    block_number = payload["block_number"]
    email = payload.get("email") or None

    try:
        public_address = extract_public_key_from_signature(block_number, signature)

        latest_block = web3_object.eth.get_block('latest')
        block_difference = abs(int(latest_block.number) - int(block_number))

        if block_difference <= BLOCK_THRESHOLD and public_address == wallet_address:
            is_registered_user = UserRepository().is_registered_user(address=wallet_address)
            if is_registered_user is None:
                agi_balance = UserRepository().check_agi_balance(wallet_address)
                if agi_balance is None:
                    message = 'You do not have any AGI in your wallet and hence this does not apply to you. If you have staked your tokens then you will automatically receive AGIX in the staking pool, so you do not need to do anything'
                else:
                    UserRepository().create_registration(wallet_address, signature, email)
                    statusCode = HTTPStatus.OK.value
                    message = HTTPStatus.OK.phrase
            else:
                message = 'You have already registered'
    except Exception as e:
        print(repr(e))
        raise e

    return statusCode, message


def submit_user_question(payload, signature):
    email = payload["email"]
    wallet_address = payload["wallet_address"]
    comment = payload["comment"]
    block_number = payload["block_number"]
    name = payload.get("name") or None

    public_address = extract_public_key(email, comment, block_number, signature)
    try:
        latest_block = web3_object.eth.get_block('latest')
        block_difference = abs(int(latest_block.number) - int(block_number))

        if block_difference <= BLOCK_THRESHOLD and public_address == wallet_address:
            CustomerComments().submit_comment(wallet_address, comment, email, name)
            statusCode = HTTPStatus.OK.value
            message = HTTPStatus.OK.phrase
        else:
            statusCode = HTTPStatus.BAD_REQUEST.value
            message = HTTPStatus.BAD_REQUEST.phrase
    except Exception as e:
        print(repr(e))
        raise e

    return statusCode, message


def extract_public_key_from_signature(block_number, signature):
    message = web3.Web3.soliditySha3(["uint256"], [int(block_number)])
    hash = defunct_hash_message(message)
    return web3_object.eth.account.recover_message(encode_defunct(hash), signature=signature)


def extract_public_key(email, plain_message, block_number, signature):
    message = web3.Web3.soliditySha3(["string", "string", "uint256"], [email, plain_message, int(block_number)])
    hash = defunct_hash_message(message)
    return web3_object.eth.account.recover_message(encode_defunct(hash), signature=signature)
