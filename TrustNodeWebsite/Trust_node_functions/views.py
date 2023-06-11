from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync, sync_to_async
import aiohttp
import json
from .models import User

# Create your views here.

@csrf_exempt
@async_to_sync
async def Trust_Node_Main(request):
    """
    1) interact with dealer so you can get the two private keys
    2)
    """
    if request.method == 'POST':
        data = json.loads(request)
        passport_number = data.POST.get('passport_number') 
        print("I AM IN 6 IN VIEWS.PY")
    
        if User.objects.filter(Passport=passport_number).exists():
            """Trust node already have this user infromation, start process without dealer"""
            return HttpResponse('Method not allowed', status=405)
            
        
        else:
            """We need to create all keys for the trust node and the user """
            payload = {
                'passport': passport_number,
                'message': "Dealer give me private key for me p and the public key for user trust node "
            }
            async with aiohttp.ClientSession() as session:
                async with session.post('http://127.0.0.1:8060', json=payload) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        
                        print(response_data)
                    #     return JsonResponse(response_data)
                    # else:
                    #     print('Error: Trust node API request failed', status=500)
                    #     return HttpResponse('Method not allowed', status=405)
            response_data = {
                'status': 'success'
            }
            return JsonResponse(response_data)
    else:
        return HttpResponse('Method not allowed', status=405)        


if __name__ == '__main__':
    Trust_Node_Main('test_function-Trust_Node_Main') 
    
    