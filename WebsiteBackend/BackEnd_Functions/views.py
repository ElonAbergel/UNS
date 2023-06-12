import json
import aiohttp
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync, sync_to_async
from .models import User
import random
from django.contrib.auth.hashers import make_password

"""
What to do register:
1) after keys are sent from dealer we need to get them and save them in trustnode and dealer node
2) start the sign token fun between the trust node of website and trust node of user 
3) check that all data is saved!/ handle errors

what to do login:
1) I am not quite sure about that 

"""


DEALER = 'http://127.0.0.1:8060'
TRUST_NODE_USER = 'http://127.0.0.1:8040'
TrustNode_Website = 'http://127.0.0.1:8080'

# Generate a random nonce of the specified length. 
def generate_nonce(length=16):
    chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    nonce = ''.join(random.choice(chars) for _ in range(length))
    return nonce

# This api request the trustnode of the user to start the Sybil Authentication
@async_to_sync
async def make_async_request_to_User_TrustNode(payload_TrustNode_User):
    async with aiohttp.ClientSession() as session:
        async with session.post(TRUST_NODE_USER + '/register/message_send', json=payload_TrustNode_User) as response:
            if response.status == 200:
                response_data = await response.json()
                response_data['status'] = 'succeed to register User'
                return JsonResponse(response_data)
            else:
                print('Error: Trust node API request failed', status=500)
                return HttpResponse('Method not allowed', status=405)


# This function deal with the api request to the dealer to send keys
@async_to_sync
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
                'message': "Dealer give me private keys and public keys for user trust node and website trust node ",
                'TrustNode_Website': TrustNode_Website,
                'TRUST_NODE_USER': TRUST_NODE_USER,
                'website_name': 'Ywitter'
                
                

            }
            # request dealer to send keys to trust nodes
            if make_async_request_to_Dealer(payload_Dealer):
                
                # We start the Sybil Authentication, sending trust node user Token T1            
                payload_TrustNode_User = {
                    'Passport': passport,
                    'TrustNode_Website': TrustNode_Website,
                    'Nonce_T1': generate_nonce()
                }

                response = await make_async_request_to_User_TrustNode(payload_TrustNode_User)
                if response['status'] == 'succeed to register User!': 
                    
                    # Encrypt the password
                    hashed_password = make_password(password)
                    # Create a new user object || save the user data!
                    user = User(name=name, email=email, password=hashed_password, passport=response['passport_w'], trustNode=trustNode)
                    
                    # Save the user to the database
                    user.save()
                    
                    return JsonResponse({'message': "succeed to register User!"})
                else:
                    return JsonResponse({'message': "Failed to register User!"})
             
    else:
        return HttpResponse('Method not allowed', status=405)


async def get_csrf_token(request):
    csrf_token = get_token(request)
    print(csrf_token)
    return JsonResponse({'token': csrf_token})


    