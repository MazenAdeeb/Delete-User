from django.shortcuts import render
from django.http import HttpResponse
import requests
from .utils import get_auth_token  # Import the utility function

def get_auth_token(username, password):
    url = 'http://mazenadeeb.pythonanywhere.com/api/accounts/api-token-auth/'  # Your token authentication endpoint
    try:
        response = requests.post(url, data={'username': username, 'password': password})
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json().get('token')
    except requests.RequestException as e:
        print(f"Error: {e}")
        raise





def delete_account(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return HttpResponse('Email and password are required.', status=400)

        try:
            # Get the auth token
            token = get_auth_token(email, password)

            # Use the token to get user details, including pk
            user_info_url = 'http://mazenadeeb.pythonanywhere.com/api/accounts/user-info/'
            headers = {
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json'
            }
            user_info_response = requests.get(user_info_url, headers=headers)
            user_info_response.raise_for_status()
            user_info = user_info_response.json()
            print("User Info Response:", user_info)  # Debug line

            # Extract pk from user info
            pk = user_info.get('id')  # Make sure to use 'id' instead of 'pk'
            if not pk:
                return HttpResponse('User ID (pk) could not be found.', status=400)

            # Your API endpoint for deleting the user
            delete_url = f'http://mazenadeeb.pythonanywhere.com/api/accounts/delete-account/{pk}'
            delete_response = requests.delete(delete_url, headers=headers)
            delete_response.raise_for_status()
            return HttpResponse('Account deletion request sent successfully.')
        except requests.RequestException as e:
            return HttpResponse(f'Error processing the request: {e}', status=500)

    return render(request, 'deletion_form.html')

