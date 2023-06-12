from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from asgiref.sync import async_to_sync, sync_to_async
import aiohttp
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.db.models import Q
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import requests




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
    else:
        return HttpResponse('Method not allowed', status=405)        



# This function start the Sybil Authentication messages signing
@async_to_sync
@csrf_exempt
async def TrustNodeUserSybil_message(request):
        if request.method == 'POST':
            data = await json.loads(request)
            # we get the data from the api call
            passport_number = data.POST.get('Passport')
            Trust_Node_Website = data.POST.get('TrustNode_Website')
            Nonce_T1 = data.POST.get('Nonce_T1')
            website_name = data.POST.get('website_name')
            try:
                # Retrieve the user with the matching passport number
                user = User.objects.get(Q(Passport=passport_number) & Q(website_name=website_name))
                
                # Access the user's information and save it to variables
                public_key = user.Public_key_Trust_Node
                private_key = user.Private_key_User
                website_name = user.website_name
                

                # converts the private key from a string format to bytes by encoding it using UTF-8. 
                private_key_bytes = private_key.encode('utf-8')
                
                # This line loads the private key from the bytes representation 
                private_key_obj = serialization.load_pem_private_key(private_key_bytes, password=None, backend=default_backend())

                # Sign the message using the private key
                signature = private_key_obj.sign(
                    Nonce_T1.encode('utf-8'),
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )

                # Convert the signature to a string
                signature_str = signature.hex()

                # Prepare the data to be sent to the Trust_Node_Website API
                api_data = {
                    'Nonce_T1': signature_str,
                    
                }
                # we 
                response = await requests.post(Trust_Node_Website + '/message_Nonce', json=api_data)

                

                
            except User.DoesNotExist:
                return HttpResponse('ISSUE User is not in the data base!', status=410)
                
                
            
    
        else:
            return HttpResponse('Method not allowed', status=405)    
        
        
        
        
        
     
    

