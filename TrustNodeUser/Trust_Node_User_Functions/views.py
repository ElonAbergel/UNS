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
from cryptography.hazmat.primitives.asymmetric import rsa



# Generate a random nonce of the specified length. 
def generate_nonce(length=16):
    chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    nonce = ''.join(random.choice(chars) for _ in range(length))
    return nonce


TRUST_NODE_USER = 'http://127.0.0.1:8040'
# This function save the keys from the website
@async_to_sync
@csrf_exempt
async def TrustNodeUserSybil_keys(request):
    
    if request.method == 'POST':
        data = await json.loads(request)
        # we get the data from the api call
        Passport = data.POST.get('passport_number')
        Public_key_Trust_Node = data.POST.get('public_key_trustnode_website')
        Public_key_User = data.POST.get('public_key_user')
        private_key_Dealer_u = data.POST.get('public_key_user')
        Website_Name = data.POST.get('website')

        # we save the data
        user = User.objects.create(
                Passport = Passport,
                Public_key_Trust_Node = Public_key_Trust_Node, 
                private_key_Dealer_u = private_key_Dealer_u,
                website_name = Website_Name,
                Public_key_User=Public_key_User
        )
        user.save()
    else:
        return HttpResponse('Method not allowed', status=405)        




def blind_passport_number(passport, private_key_Dealer_u):

    # Convert the private key and passport from string format to bytes
    private_key_bytes = private_key_Dealer_u.encode('utf-8')
    passport_bytes = passport.encode('utf-8')

    
    # Encrypt the passport and private key with nonce_nm together using the private_key_user
    encrypted_data = private_key_Dealer_u().encrypt(
        passport_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ),
        private_key_Dealer_u
    )

    # Convert the encrypted data to a string
    encrypted_data_str = encrypted_data.hex()

    return encrypted_data_str
    
@async_to_sync
@csrf_exempt
async def TrustNodeUserSybil_message(request):
    if request.method == 'POST':
        data = await json.loads(request)
        # Get the data from the API call
        passport_number = data.POST.get('Passport')
        Trust_Node_Website = data.POST.get('TrustNode_URL')
        # Nonce_T1 = data.POST.get('Nonce_T1')
        website_name = data.POST.get('website_name')
        try:
            # Retrieve the user with the matching passport number
            user = User.objects.get(Q(Passport=passport_number) & Q(website_name=website_name))

            # Access the user's information and save it to variables
            public_key_user = user.Public_key_User
            public_key_trust_Node = user.Public_key_Trust_Node
            private_key_Dealer_u = user.private_key_Dealer_u
            website_name = user.website_name
            
                # we will read the private key and a public key of a user:
            # Read the private key from the PEM file
            # with open('private_key.pem', 'rb') as private_key_file:
            #     private_key_pem = private_key_file.read()
            #             # Parse the private key from PEM format
            # private_key_user = serialization.load_pem_private_key(
            #     private_key_pem,
            #     password=None,
            #     backend=default_backend()
            # )
            # we assume this nonce also inculde the one the user signed on 
            nonce_n = generate_nonce()
            PN_ = blind_passport_number(passport_number, private_key_Dealer_u)

            # Convert the blinded passport number and nonce to bytes
            # encrypted_data_str_for_sign = encrypted_data_str.encode('utf-8')
            

            # # Sign the token data using the private key
            # signature = private_key_user.sign(
            #     encrypted_data_str_for_sign,
            #     padding.PSS(
            #         mgf=padding.MGF1(hashes.SHA256()),
            #         salt_length=padding.PSS.MAX_LENGTH
            #     ),
            #     hashes.SHA256()
            # )

            # # Convert the signature to a string
            # signature_str = signature.hex()

            # Prepare the data to be sent to the Trust_Node_Website API
            T_2 = {
                'passport_number': passport_number,
                'PN': PN_,
                'N_Noce':nonce_n,
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
        
        
        
        
        
     