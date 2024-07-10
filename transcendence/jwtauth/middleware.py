from django.urls import resolve
import jwt
from datetime import datetime, timezone
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.http import JsonResponse

class JWTMiddleware(MiddlewareMixin):

    def process_request(self, request):
        protected_endpoints = [
            'search', 
            'add_friend', 
            'remove_friend', 
            'profile',
        ]
        resolver_match = resolve(request.path_info)
        endpoint = resolver_match.url_name

        if endpoint in protected_endpoints:
            auth_header = request.META.get('HTTP_AUTHORIZATION', None)

            if auth_header is None:
                access_token = request.session.get('jwt_access')
                if access_token:
                    auth_header = f'Bearer {access_token}'
                    request.META['HTTP_AUTHORIZATION'] = auth_header

            if auth_header:
                try:
                    token = auth_header.split(' ')[1]
                    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                    exp = datetime.fromtimestamp(decoded_token['exp'], tz=timezone.utc)

                    if exp < datetime.now(tz=timezone.utc):
                        raise jwt.ExpiredSignatureError("Access token has expired")

                except jwt.ExpiredSignatureError:
                    print("Access token expired, refreshing token...")
                    refresh_token = request.session.get('jwt_refresh')
                    if refresh_token:
                        try:
                            new_tokens = self.refresh_access_token(refresh_token)
                            request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_tokens["access"]}'
                            request.session['jwt_refresh'] = new_tokens["refresh"]
                            request.session['jwt_access'] = new_tokens["access"]
                            print("Tokens have bee refreshed, authorization header was set...")
                        except TokenError as e:
                            print(f"Error refreshing token: {str(e)}")
                            return JsonResponse({'error': str(e)}, status=401)
                    else:
                        print("No refresh token available, cannot refresh access token.")
                        return JsonResponse({'error': 'No refresh token available'}, status=401)
                except (jwt.DecodeError, TokenError) as e:
                    print(f"Token error: {str(e)}")
                    return JsonResponse({'error': str(e)}, status=401)
            else:
                print("Authorization header and session access token both missing.")
                return JsonResponse({'error': 'Authorization header missing'}, status=401)

    def refresh_access_token(self, refresh_token):
        refresh = RefreshToken(refresh_token)
        new_access_token = refresh.access_token
        new_tokens = {
            "access": str(new_access_token),
            "refresh": str(refresh),
        }
        return new_tokens
    