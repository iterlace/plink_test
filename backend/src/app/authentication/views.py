import json

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import SignUpRequest
from .serializers import SignUpSerializer
from .helpers import get_client_ip


@csrf_exempt
@require_http_methods(["POST"])
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

    ip = get_client_ip(request)
    c = serializer.save(ip_addr=ip)
    return JsonResponse({"error": False, "entry": serializer.data})


@require_http_methods(["GET"])
def my_requests(request: HttpRequest) -> JsonResponse:
    ip = get_client_ip(request)
    requests = SignUpRequest.objects.filter(ip_addr=ip)
    serializer = SignUpSerializer(
        requests,
        many=True,
    )
    return JsonResponse({"entries": serializer.data})
