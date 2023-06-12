import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync, sync_to_async
from .models import Dealer
from Crypto.Util.number import getPrime, inverse
import random
import requests
import math

@async_to_sync
@csrf_exempt
async def Generate_Keys(request):
    """
    Here we need to check if the user passport already has a key and related stuff
    """
    if request.method == 'POST':
        data = await json.loads(request)
        
        passport_number = data.POST.get('passport_number') 
        Website_Name = data.POST.get('website_name')
        user_trust_node_url =  data.POST.get('TRUST_NODE_USER') + 'register/user_keys/'
        website_trust_node_url = data.POST.get('TrustNode_Website') + '/register/website_keys/'   

        # Step 1: Choose a safe prime
        p = 3689348800710697289
        
        # Step 2: Choose r and u from Z(φ(p))
        phi_p = p - 1
        r = random.randint(2, phi_p - 1)
        
        # Choose a random value for Private_key_u and ensure it is coprime with phi_p
        while True:
            Private_key_u = random.randint(2, phi_p - 1)
            if math.gcd(Private_key_u, phi_p) == 1:
                break
        
        # Step 3: Calculate v = r * u^(-1) mod φ(p)
        Private_key_v = (r * inverse(Private_key_u, phi_p)) % phi_p
        
        # step 4: Calculate public keys for P and Q:
        public_key_u = pow(2, Private_key_u, p)
        public_key_v = pow(2, Private_key_v, p)
        
        print(public_key_u, public_key_v, Private_key_u, Private_key_v, r)
        
            # Save the generated keys to the dealer model
        dealer = Dealer.objects.create(
                Passport= passport_number,
                Public_key_user=public_key_u,
                Private_key_user=Private_key_u,
                Public_key_TrustNode_Website=Private_key_v ,
                Private_key_TrustNode_Website=public_key_v,
                Dealer_Key=r,
                Website = Website_Name,
            )
        dealer.save()
            
            
            # Prepare the keys to send to the trust nodes
        trust_node_user_keys = {
                'website':dealer.Website,
                'passport_number':dealer.Passport,
                'public_key': dealer.Public_key_TrustNode_Website,
                'private_key': dealer.Private_key_user
            }
        trust_node_website_keys = {
                'website': dealer.Website,
                'passport_number':dealer.Passport,
                'public_key': dealer.Public_key_user,
                'private_key': dealer.Private_key_TrustNode_Website
            }
            
        # Send the keys to the trust nodes' APIs
         
        user_trust_node_response = requests.post(user_trust_node_url, json=trust_node_user_keys)
        if user_trust_node_response.status_code != 200:
            # Handle error if needed
            pass

        # Send the website trust node keys
        website_trust_node_response = requests.post(website_trust_node_url, json=trust_node_website_keys)
        if website_trust_node_response.status_code != 200:
            # Handle error if needed
            pass
        
        return JsonResponse({'message': "All keys are good to go!"})

    else:
        return HttpResponse('Method not allowed', status=405)        
    
    
    

# if __name__ == '__main__':
#     payload_TrustNode_User = {
#     'Passport': '12345678',
#     'TrustNode_Website': 'http://127.0.0.1:8080',
#     'TRUST_NODE_USER': 'http://127.0.0.1:8040',
#     'Nonce_T1': '3F2dW7s9E1IjA5vT'
# }
#     Generate_Keys(payload_TrustNode_User) 