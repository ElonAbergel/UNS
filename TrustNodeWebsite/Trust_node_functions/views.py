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

async def Verifies(public_key_user,Nonce_T2):
    public_key_bytes = public_key_user.encode('utf-8')
    public_key_obj = serialization.load_pem_public_key(public_key_bytes, backend=default_backend())
    signature = bytes.fromhex(Nonce_T2)
    try:
        public_key_obj.verify(
            signature,
            Nonce_T2.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Signature is valid")
        return True
    except InvalidSignature:
        print("Signature is invalid")
        return False

    
    

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

async def TrustNodeWebsiteSybil_message(request):
        if request.method == 'POST':
            data = await json.loads(request)
            # we get the data from the api call
            passport_number = data.POST.get('passport_number')
            signature = data.POST.get('signature')
            website_name = data.POST.get('website_name')
            blinded_passport = data.POST.get('blinded_passport')
            TRUST_NODE_USER = data.POST.get('Trust_Node_User')
                
            try:
                     
                # Retrieve the user with the matching passport number
                user = User.objects.get(Q(Passport=passport_number) & Q(website_name=website_name))
                    
                # Access the user's information and save it to variables
                public_key_user = user.Public_key_user
                private_key = user.Private_key_TrustNode
                
                # We verify the public key 
                if(Verifies(public_key_user,signature)):
                    
                    PN_blinded = blind_passport_number(blinded_passport, private_key)
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

                    response_data = {
                    'message': 'Succeed to register User!',
                    'passport_number': passport_number,
                    'signature': signature_str,
                    'blinded_passport': PN_blinded,
                    'website_name': website_name
}
                
                    return JsonResponse(response_data)

                
                
                else:
                    return HttpResponse('Issue InvalidSignature ', status=411)
                    
                    
        

                

                
            except User.DoesNotExist:
                return HttpResponse('Issue InvalidSignature ', status=410)
                
                
            
        
        
        
        
        
        
        
        
        
        
        
        