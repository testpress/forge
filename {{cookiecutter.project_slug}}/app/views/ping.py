from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app.tasks import ping

@csrf_exempt
def trigger_ping_task(request):
    if request.method == "POST":
        result = ping.delay()
        return JsonResponse({"task_id": result.id})
    return JsonResponse({"error": "Only POST allowed"}, status=405)
