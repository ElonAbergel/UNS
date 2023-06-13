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
from cryptography.exceptions import InvalidSignature

# Create your views here.



    
    

@csrf_exempt
@async_to_sync
async def TrustNodeWebsiteSybil_keys(request):
    """
    1) interact with dealer so you can get the two private keys and public
    2)
    """
    if request.method == 'POST':
        data = await json.loads(request)
        # we get the data from the api call
        Passport = data.POST.get('passport_number')
        Public_key_user = data.POST.get('public_key_user')
        Private_key_TrustNode = data.POST.get('private_key_trustnode')
        Website_Name = data.POST.get('website')
        Public_key_Trust_Node = data.POST.get('public_key_trustnode_website')

        # we save the data
        user = User.objects.create(
                Passport = Passport,
                Public_key_user = Public_key_user, 
                Private_key_TrustNode = Private_key_TrustNode,
                website_name = Website_Name,
                Public_key_Trust_Node =Public_key_Trust_Node
        )
        user.save()
        
    else:
        return HttpResponse('Method not allowed', status=405)  
    

# async def Verifies(public_key_user, signature):
    
#     # Convert the signature from string to bytes
#     signature_str = bytes.fromhex(signature)
    
#     try:
#         # Verify the signature
#         public_key_user.verify(
#             bytes.fromhex(signature),
#             b"verification_message",
#             padding.PKCS1v15(),
#             hashes.SHA256()
#         )
        
        
#         return True, "Signature is valid"
#     except InvalidSignature:
#         return False, "Signature is invalid"


# def decrypt_blinded_passport(encrypted_data_str, public_key_user):
#     # Convert the encrypted data from string format to bytes
#     encrypted_data = bytes.fromhex(encrypted_data_str)

#     try:
#         # Decrypt the encrypted data using the public_key_user
#         decrypted_data = public_key_user.decrypt(
#             encrypted_data,
#             padding.OAEP(
#                 mgf=padding.MGF1(algorithm=hashes.SHA256()),
#                 algorithm=hashes.SHA256(),
#                 label=None
#             )
#         )

#         # Split the decrypted data into passport and private key
#         PN_length = len(decrypted_data) // 2
#         PN = decrypted_data[:PN_length].decode('utf-8')
#         nonce_n = decrypted_data[PN_length:].decode('utf-8')

#         return PN, nonce_n
#     except (ValueError, TypeError, InvalidSignature):
#         # Handle decryption errors
#         return None, None
    

def blind_passport_number(passport, private_key_trustnode_v):

    # Convert the private key and passport from string format to bytes
    private_key_bytes = private_key_trustnode_v.encode('utf-8')
    passport_bytes = passport.encode('utf-8')

    
    # Encrypt the passport and private key with nonce_nm together using the private_key_user
    encrypted_data = private_key_trustnode_v().encrypt(
        passport_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ),
        private_key_trustnode_v
    )

    # Convert the encrypted data to a string
    encrypted_data_str = encrypted_data.hex()

    return encrypted_data_str


async def TrustNodeWebsiteSybil_message(request):
        if request.method == 'POST':
            data = await json.loads(request)
            # we get the data from the api call
            passport_number = data.POST.get('passport_number')
            # signature = data.POST.get('signature')
            website_name = data.POST.get('website_name')
            TRUST_NODE_USER = data.POST.get('Trust_Node_User')
                
            try:
                     
                # Retrieve the user with the matching passport number
                user = User.objects.get(Q(Passport=passport_number) & Q(website_name=website_name))
                    
                # Access the user's information and save it to variables
            
                private_key_trustnode_v = user.Private_key_TrustNode
                
                # We verify the public key 
                # blinded_passport = Verifies(signature,blinded_passport_bytes)
                    
                # Read the public key from the PEM file or any other storage
                # with open('public_key.pem', 'rb') as public_key_file:
                #     public_key_pem = public_key_file.read()

                # # Parse the public key from PEM format
                # public_key_user = serialization.load_pem_public_key(
                #     public_key_pem,
                #     backend=default_backend()
                # )
                
                # encrypted_message = public_key_user,data.POST.get('decrypt_message')
                # # we need to decrypt the message so we can blind it with second key
                # PN, nonce_n =  decrypt_blinded_passport(encrypted_message,public_key_user)
                PN_1_2 = data.POST.get('PN')
                N_Nonce = data.POST.get('N_Noce')
                PN_blinded = blind_passport_number(PN_1_2, private_key_trustnode_v)

                
                            # Prepare the data to be sent to the website N nd PN'' 

                response_data = {
                'message': 'Succeed to register User!',
                'passport_number': passport_number,
                'blinded_passport': PN_blinded,
                'N_Nonce': N_Nonce,
                'website_name': website_name,
}
            
                return JsonResponse(response_data)

                
                    
        
                
            except User.DoesNotExist:
                return HttpResponse('Issue InvalidSignature ', status=410)
                
                
            
        
        
        
        
        
        
        
        
        
        
        
        