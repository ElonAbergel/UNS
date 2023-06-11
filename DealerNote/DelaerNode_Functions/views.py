import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync, sync_to_async
from .models import Dealer
from Crypto.Util.number import getPrime, inverse
import random
import requests

# Function to generate a safe prime
def generate_safe_prime(bits):
    while True:
        prime = getPrime(bits)
        if (prime - 1) % 2 == 0 and getPrime((prime - 1) // 2):
            return prime

@csrf_exempt
def Generate_Keys(request):
    """
    Here we need to check if the user passport already has a key and related stuff
    """
    if request.method == 'POST':
        data = json.loads(request)
        passport_number = data.POST.get('passport_number') 

        # Step 1: Choose a safe prime
        p = generate_safe_prime(1024)
        
        
        # Step 2: Choose r and u from Z(φ(p))
        phi_p = p - 1
        r = random.randint(2, phi_p - 1)
        Private_key_u = random.randint(2, phi_p - 1)
        

        # Step 3: Calculate v = r * u^(-1) mod φ(p)
        Private_key_v = (r * inverse(Private_key_u, phi_p)) % phi_p
        
        
        # step 4: Calculate public keys for P and Q:
        public_key_u = pow(2, Private_key_u, p)
        public_key_v = pow(2, Private_key_v, p)
        
        
        # Save the generated keys to the dealer model
        dealer = Dealer.objects.create(
            Passport= str(passport_number),
            Public_key_user=str(public_key_u),
            Private_key_user= str(Private_key_u),
            Public_key_TrustNode_Website= str(Private_key_v) ,
            Private_key_TrustNode_Website=str(public_key_v),
            Dealer_Key=r
        )
        dealer.save()
        
        
        # Prepare the keys to send to the trust nodes
        trust_node_user_keys = {
            'public_key': dealer.Public_key_TrustNode_Website,
            'private_key': dealer.Private_key_user
        }
        trust_node_website_keys = {
            'public_key': dealer.Public_key_user,
            'private_key': dealer.Private_key_TrustNode_Website
        }
        
        # Send the keys to the trust nodes' APIs
        user_trust_node_url = 'http://localhost:8040/api/user_keys/'
        website_trust_node_url = 'http://localhost:8080/api/website_keys/'
        
        user_trust_node_response = requests.post(user_trust_node_url, json=trust_node_user_keys)
        if user_trust_node_response.status_code != 200:
            # Handle error if needed
            pass

        # Send the website trust node keys
        website_trust_node_response = requests.post(website_trust_node_url, json=trust_node_website_keys)
        if website_trust_node_response.status_code != 200:
            # Handle error if needed
            pass



    else:
        return HttpResponse('Method not allowed', status=405)        
    
    
