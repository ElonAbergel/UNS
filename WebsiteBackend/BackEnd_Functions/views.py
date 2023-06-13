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
Done 1) after keys are sent from dealer we need to get them and save them in trustnode and dealer node
2) start the sign token fun between the trust node of website and trust node of user 
3) check that all data is saved!/ handle errors

what to do login:
1) I am not quite sure about that 

"""

"""IDEAS
We can pass the user private key, just to show prove of signing douments
we can assume that all data is been signed and approved
"""


DEALER = 'http://127.0.0.1:8060'
TRUST_NODE_USER = 'http://127.0.0.1:8040'
TrustNode_URL = 'http://127.0.0.1:8080'

# # Generate a random nonce of the specified length. 
# def generate_nonce(length=16):
#     chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
#     nonce = ''.join(random.choice(chars) for _ in range(length))
#     return nonce


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
        """
        We can assume that the user singed with his private key send it  
        to his Trust node and verified everything:
         
        option, to hard code private keys for user and 
        have the public keys in the trust node
        
        """
        # private_key_user = data.get('private_key_user')
        
        # Check if the user exists in the database with the given passport
        try:
            user_check = User.objects.get(passport=passport)
            return JsonResponse({'message': "Denied the user is already in the database!"})
        
       
        except User.DoesNotExist:
            # We register the user to the Sybil Authentication
            
            payload_Dealer = { # Construct the request payload
                'passport': passport,
                'message': "Dealer give me private keys(v and u) for user trust node and website trust node ",
                'TrustNode_Website': TrustNode_URL,
                'TRUST_NODE_USER': TRUST_NODE_USER,
                'website_name': 'Ywitter'
                
                
            }
            # request dealer to send keys to trust nodes
            if make_async_request_to_Dealer(payload_Dealer):
                
                """
                We are just gonna skip to step 2:
                UT generates a new token (T2), adds to it the same nonce N and a blinded version (PN') of the user's passport number (PN), and signs with its own private key. Note that PN' = E(PN, P).

                Assume that all trust nodes, including UT and WT, know each other's public keys and can 
                verify each other's signatures.  

                UT sends T2 to WT. 
                
                WT extracts PN' and N.  
                
                WT completes the blinding of PN' to PN'' using the 
                second key Q.
                
                WT provides N and PN'' to W.  Note that PN'' = E(PN', Q).
                W now has a stable commitment of U's identity that will remain the 
                same regardless of which trust node U chooses.  
                    """
                # We start the Sybil Authentication, sending trust node user Token T1            
                payload_TrustNode_User = {
                    'Passport': passport,
                    'TrustNode_URL': TrustNode_URL,
                    'website_name': 'Ywitter'
                }

                response = await make_async_request_to_User_TrustNode(payload_TrustNode_User)
                if response['message'] == 'succeed to register User!': 
                    
                    # Encrypt the password
                    hashed_password = make_password(password)
                    # Create a new user object || save the user data!
                    user = User(name=str(name), email=str(email), password=str(hashed_password), passport=response['blinded_passport'], trustNode=trustNode)
                    
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


    