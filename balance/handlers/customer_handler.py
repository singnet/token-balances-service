from common.format_response import format_response


def submit_question(event, context):
    statusCode = 200
    message = "You have submitted your query successfully"

    return format_response(statusCode, message)
