import web3

from eth_account.messages import defunct_hash_message, encode_defunct
from infrastructure.repository.customer_comments_repo import CustomerComments
from http import HTTPStatus
from web3 import Web3
from config import HTTP_PROVIDER

web3_object = Web3(web3.providers.HTTPProvider(HTTP_PROVIDER))


def submit_user_question(payload, signature):
    email = payload["email"]
    address = payload["wallet_address"]
    comment = payload["comment"]
    block_number = payload["block_number"]
    name = payload.get("name") or None
    message = payload["message"]
    public_key = extract_public_key(email=email, plain_message=message, block_number=block_number, signature=signature)

    if public_key == address:
        CustomerComments().submit_comment(address, comment, email, name)
        statusCode = HTTPStatus.OK.value
        message = HTTPStatus.OK.phrase
    else:
        statusCode = HTTPStatus.BAD_REQUEST.value
        message = HTTPStatus.BAD_REQUEST.phrase

    return statusCode, message


def extract_public_key(email, plain_message, block_number, signature):
    message = web3.Web3.soliditySha3(["string", "string", "uint256"], [email, plain_message, int(block_number)])
    hash = defunct_hash_message(message)
    return web3_object.eth.account.recover_message(encode_defunct(hash), signature=signature)
