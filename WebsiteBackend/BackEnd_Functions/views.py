import json
import aiohttp
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync, sync_to_async
from .models import User

DEALER = 'http://127.0.0.1:8060'

async def make_async_request_to_User_TrustNode(payload):
    async with aiohttp.ClientSession() as session:
        # headers = {'X-CSRFToken': 'Nave_Abergel'}  # Include the CSRF cookie in the headers
        async with session.post('http://127.0.0.1:8080', json=payload) as response:
            if response.status == 200:
                response_data = await response.json()
                response_data['status'] = 'succeed to register User'
                
                return JsonResponse(response_data)
            else:
                print('Error: Trust node API request failed', status=500)
                return HttpResponse('Method not allowed', status=405)

async def make_async_request_to_Dealer(payload_Dealer):
    async with aiohttp.ClientSession() as session:
        async with session.post(DEALER, json=payload_Dealer) as response:
            if response.status == 200:
                response_data = await response.json()
                if response_data['message'] == 'All keys are good to go!':
                    return True
                else:
                    print(response_data)
                    return False
            else:
                print(" not sure what's going on")
                return False
    
    

@csrf_exempt
@async_to_sync
async def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        passport = data.get('passport')
        trustNode = data.get('trustNode')
        
        # Check if the user exists in the database with the given passport
        try:
            user_check = User.objects.get(passport=passport)
            return JsonResponse({'message': "Denied the user is already in the database!"})
        
       
        except User.DoesNotExist:
            
            # We register the user to the Sybil Authentication
            
            payload_Dealer = { # Construct the request payload
                'passport': passport,
                'message': "Dealer give me private keys and public keys for user trust node and website trust node "
            }
            # request dealer to send keys to trust nodes
            if make_async_request_to_Dealer(payload_Dealer):
                
                # We start the Sybil Authentication, sending trust node user Token T1            
            # payload_ = {
            #     'passport': passport,
            #     'trustNode': 'http://127.0.0.1:8080'
            # }

            response = await make_async_request(payload)
            if response['status'] == 'succeed to register User':
                
                
    else:
        return HttpResponse('Method not allowed', status=405)


async def get_csrf_token(request):
    csrf_token = get_token(request)
    print(csrf_token)
    return JsonResponse({'token': csrf_token})


    