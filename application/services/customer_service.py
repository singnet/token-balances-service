import web3

from eth_account.messages import defunct_hash_message, encode_defunct
from infrastructure.repository.customer_comments_repo import CustomerComments
from http import HTTPStatus
from web3 import Web3
from config import HTTP_PROVIDER, BLOCK_THRESHOLD

web3_object = Web3(web3.providers.HTTPProvider(HTTP_PROVIDER))


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

        if block_difference <= BLOCK_THRESHOLD and public_address.lower() == wallet_address.lower():
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


def extract_public_key(email, plain_message, block_number, signature):
    message = web3.Web3.soliditySha3(["string", "string", "uint256"], [email, plain_message, int(block_number)])
    hash = defunct_hash_message(message)
    return web3_object.eth.account.recover_message(encode_defunct(hash), signature=signature)

