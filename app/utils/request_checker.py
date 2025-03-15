from flask import request

def request_json_contains(required_fields: tuple[str]) -> bool:
    return request.json != None and not all(k in request.json for k in required_fields)