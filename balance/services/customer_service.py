from infrastructure.repository.customer_respository import Customer

customer = Customer()


def submit_user_question(address, email, comment, name=None):
    customer.submit_comment(address, comment, email, name)
    statusCode = 200
    message = "Submitted comment successfully"
    return statusCode, message