from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.

def Trust_Node_Main(request):
    print("I AM IN 6 IN VIEWS.PY")
    response_data = {
        'status': 'success'
    }
    return JsonResponse(response_data)