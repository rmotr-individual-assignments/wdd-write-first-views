from django.http import HttpResponse


def app_status(request):
    response = HttpResponse(content_type='application/json')
    response.status_code = 200
    response.content = '{"status": "OK"}'
    return response
