from django.shortcuts import render
import json
import aiohttp
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync, sync_to_async
from .models import User

@csrf_exempt
def Generate_Keys(request):
    """
    Here we need to check if the user passport already has a key and related stuff
    """
    if request.method == 'POST':
        data = json.loads(request)
        passport_number = data.POST.get('passport_number') 

        # try:
        #     # Check if a user with the given passport number exists in the database
        #     user = User.objects.get(Passport=passport_number)
        #     public_key = user.Public_key_user

        #     # response_data = {
        #     #     'status': 'success',
        #     #     'public_key': public_key
        #     # }

        # except User.DoesNotExist:
            # Generate a new key pair for the user
            # ... your code to generate the key pair

            # Save the new user to the database
        # user = User(Passport=passport_number, Public_key=public_key)
        # user.save()

        response_data = {
            'status': 'success',
            'public_key': "public_key"
        }

        return JsonResponse(response_data)
    else:
        return HttpResponse('Method not allowed', status=405)        