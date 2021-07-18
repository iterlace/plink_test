import json

from authentication.serializers import SignUpSerializer
from django.http import HttpRequest, JsonResponse


def signup(request: HttpRequest) -> JsonResponse:
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": True}, status=400)

    serializer = SignUpSerializer(data=body)
    if not serializer.is_valid():
        return JsonResponse(
            {
                "error": True,
                "details": serializer.errors,
            },
            status=400,
        )

    return JsonResponse({"error": False})
