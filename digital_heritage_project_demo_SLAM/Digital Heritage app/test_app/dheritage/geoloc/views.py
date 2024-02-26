from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from django.http import JsonResponse

@csrf_exempt  # Use this decorator to disable CSRF protection for this view, or handle CSRF token in your C++ application.
# def update_current(request):
#     if request.method == 'GET':
#         try:
#             # Extract data from GET request parameters
#             x = float(request.GET.get('x'))
#             y = float(request.GET.get('y'))
#             yaw = float(request.GET.get('yaw'))

#             # Perform any processing with the received data
#             # ...

#             # Respond with a success message
#             response_data = {'status': 'success'}
#             return JsonResponse(response_data)
#         except Exception as e:
#             # Handle errors, log them, and respond with an error message
#             response_data = {'status': 'error', 'message': str(e)}
#             return JsonResponse(response_data, status=400)

#     # If the request method is not GET, respond with an error
#     return JsonResponse({'status': 'error', 'message': 'Only GET requests are allowed'}, status=405)

@csrf_exempt
def update_current(request):
    if request.method == 'POST':
        try:
            # Extract text data from the request
            text_data = request.body.decode('utf-8')  # Assuming UTF-8 encoding

            # Perform any processing with the received text data
            # ...

            # Respond with a success message
            response_data = 'Data received successfully'
            return HttpResponse(response_data, content_type='text/plain')
        except Exception as e:
            # Handle errors, log them, and respond with an error message
            error_message = str(e)
            return HttpResponse(error_message, content_type='text/plain', status=500)

    # If the request method is not POST, respond with an error
    return HttpResponse('Method Not Allowed', status=405)

def index(request):
    return render(request, 'index.html')