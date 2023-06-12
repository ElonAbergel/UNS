from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from asgiref.sync import async_to_sync, sync_to_async
import aiohttp
from django.views.decorators.csrf import csrf_exempt
from .models import User


# This function save the keys from the website
@async_to_sync
@csrf_exempt
async def TrustNodeUserSybil_keys(request):
    
    if request.method == 'POST':
        data = await json.loads(request)
        # we get the data from the api call
        Passport = data.POST.get('passport_number')
        Public_key_Trust_Node = data.POST.get('public_key')
        Private_key_User = data.POST.get('private_key')
        Website_Name = data.POST.get('website')

        # we save the data
        user = User.objects.create(
                Passport = Passport,
                Public_key_Trust_Node = Public_key_Trust_Node, 
                Private_key_User = Private_key_User,
                website_name = Website_Name,
        )
        user.save()
        
        
        
        
        
     
    

