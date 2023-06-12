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
import random


TRUST_NODE_USER = 'http://127.0.0.1:8040'
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


def blind_passport_number(passport, private_key):
    # Import the necessary cryptography modules


    # Convert the private key and public key from string format to bytes
    private_key_bytes = private_key.encode('utf-8')


    # Load the private key and public key from the bytes representations
    private_key_obj = serialization.load_pem_private_key(private_key_bytes, password=None, backend=default_backend())

    # Convert the passport number to bytes
    passport_bytes = passport.encode('utf-8')

    # Blind the passport number using the public key
    blinded_passport = private_key_obj.encrypt(
        passport_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Convert the blinded passport number to a string
    blinded_passport_str = blinded_passport.hex()

    return blinded_passport_str
    
@async_to_sync
@csrf_exempt
async def TrustNodeUserSybil_message(request):
    if request.method == 'POST':
        data = await json.loads(request)
        # Get the data from the API call
        passport_number = data.POST.get('Passport')
        Trust_Node_Website = data.POST.get('TrustNode_Website')
        Nonce_T1 = data.POST.get('Nonce_T1')
        website_name = data.POST.get('website_name')
        try:
            # Retrieve the user with the matching passport number
            user = User.objects.get(Q(Passport=passport_number) & Q(website_name=website_name))

            # Access the user's information and save it to variables
            public_key_user = user.Public_key_Trust_Node
            private_key = user.Private_key_User
            website_name = user.website_name

            PN_blinded = blind_passport_number(passport_number, private_key)

            # Convert the blinded passport number and nonce to bytes
            blinded_passport_bytes = PN_blinded.encode('utf-8')
            

            
            # Load the private key from the bytes representation
            private_key_obj = serialization.load_pem_private_key(private_key.encode('utf-8'), password=None,
                                                                backend=default_backend())

            # Sign the token data using the private key
            signature = private_key_obj.sign(
                blinded_passport_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            # Convert the signature to a string
            signature_str = signature.hex()

            # Prepare the data to be sent to the Trust_Node_Website API
            T_2 = {
                'passport_number': passport_number,
                'signature': signature_str,
                'blinded_passport': PN_blinded,
                'website_name': website_name,
                'Trust_Node_User': TRUST_NODE_USER
            }

            response = await requests.post(Trust_Node_Website + '/message_T2', json=T_2)
            
            response_final = {
                'message': 'succeed to register User!',
                'blinded_passport':response['blinded_passport'],
            }
            return JsonResponse(response_final)

        except User.DoesNotExist:
            return HttpResponse('ISSUE User is not in the database!', status=410)

    else:
        return HttpResponse('Method not allowed', status=405) 
        
        
        
        
        
     
    

