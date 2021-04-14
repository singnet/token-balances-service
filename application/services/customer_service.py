from infrastructure.repository.customer_comments_repo import CustomerComments
from http import HTTPStatus

comments = CustomerComments()


def submit_user_question(payload):
    email = payload["email"]
    address = payload["wallet_address"]
    comment = payload["comment"]
    name = payload.get("name") or None
    comments.submit_comment(address, comment, email, name)
    statusCode = HTTPStatus.OK.value
    message = HTTPStatus.OK.phrase
    return statusCode, message
