from datetime import datetime
from rest_framework.response import Response


def build_response(data=None, message="", status_code=200, response_type="success"):
    if data is None:
        data = []
    return Response(
        data={
            "data": data,
            "message": message,
            "status_code": status_code,
            "type": response_type,
            "time_stamp": datetime.utcnow().isoformat() + "Z"
        },
        status=status_code
    )
