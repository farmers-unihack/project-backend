from flask import request

def safe_json(field_name: str) -> str:
    if request.json == None:
        raise ValueError("No json provided in the request")

    if field_name not in request.json:
        raise ValueError(f"The field {field_name} was not provided.")

    return request.json[field_name]

