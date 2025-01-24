from my_app import settings
from requests_oauthlib import OAuth2Session
from django.shortcuts import redirect
from django.http import JsonResponse
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

redirect_uri = 'http://localhost:8000/callback'
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

def home(request):
    return JsonResponse({'message': 'Welcome to the home page'})

def login(request):
    oa_session = OAuth2Session(settings.GITHUB_CLIENT_ID, redirect_uri=redirect_uri)
    authorization_url, state = oa_session.authorization_url(authorization_base_url)
    request.session['oauth_state'] = state
    return redirect(authorization_url)

def callback(request):
    if 'oauth_state' not in request.session:
        return JsonResponse({'error': 'Session state not found'}, status=400)
    
    if request.GET.get('state') != request.session['oauth_state']:
        request.session.flush()
        return JsonResponse({'error': 'State mismatch'}, status=400)
    try:
        github = OAuth2Session(settings.GITHUB_CLIENT_ID, state=request.session['oauth_state'], redirect_uri=redirect_uri)
        token = github.fetch_token(token_url, client_secret=settings.GITHUB_CLIENT_SECRET, authorization_response=request.build_absolute_uri())
        request.session['oauth_token'] = token
        return JsonResponse({'message': 'Successfully authenticated'})
    except Exception as e:
        request.session.flush()
        return JsonResponse({'error': str(e)}, status=400)

def profile(request):
    if 'oauth_token' not in request.session:
        return redirect('login')
    
    github = OAuth2Session(settings.GITHUB_CLIENT_ID, token=request.session['oauth_token'])
    user_info = github.get('https://api.github.com/user').json()
    return JsonResponse(user_info)

def logout(request):
    # Clear the session data
    request.session.flush()
    # Redirect to the home page or login page
    return redirect('/')