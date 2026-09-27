from django.http import HttpRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app.tasks import ping


@csrf_exempt
def trigger_ping_task(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        message = ping.send()
        return JsonResponse({"task_id": message.message_id})
    return JsonResponse({"error": "Only POST allowed"}, status=405)
