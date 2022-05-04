import json


def json_response(msg, code, error="None"):
    """
    Takes parameter and return response in json format
    :param msg: string
    :param code: string
    :param error: string
    :return: Dict
    """
    return {
        'statusCode': code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({"message": msg, 'error': error})
    }
