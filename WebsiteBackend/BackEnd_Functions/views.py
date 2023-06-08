import json
import aiohttp
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync, sync_to_async


async def make_async_request(payload):
    async with aiohttp.ClientSession() as session:
        headers = {'X-CSRFToken': 'Nave_Abergel'}  # Include the CSRF cookie in the headers
        async with session.post('http://127.0.0.1:8080', json=payload, headers=headers) as response:
            if response.status == 200:
                response_data = await response.json()
                response_data['status'] = 'success'
                
                return JsonResponse(response_data)
            else:
                print('Error: Trust node API request failed', status=500)
                return HttpResponse('Method not allowed', status=405)

@csrf_exempt
@async_to_sync
async def register_view(request):
    print("I AM IN 19 IN VEIWS.PY csrf")
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        passport = data.get('passport')
        trustNode = data.get('trustNode')

        """
        summary_line
        
        We need to send a request to the trust node API and wait for an approval message.
        """

        # Construct the request payload
        payload = {
            'passport': passport,
            'trustNode': 'http://127.0.0.1:8040'
        }

        response = await make_async_request(payload)
        return response
    else:
        return HttpResponse('Method not allowed', status=405)


async def get_csrf_token(request):
    csrf_token = get_token(request)
    print(csrf_token)
    return JsonResponse({'token': csrf_token})


    