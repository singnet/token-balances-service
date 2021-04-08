from infrastructure.repository.customer_respository import Customer
from http import HTTPStatus

customer = Customer()


def submit_user_question(address, email, comment, name=None):
    customer.submit_comment(address, comment, email, name)
    statusCode = HTTPStatus.OK.value
    message = HTTPStatus.OK.phrase
    return statusCode, message
