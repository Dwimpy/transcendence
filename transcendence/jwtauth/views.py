from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.http import JsonResponse

# class ProtectedView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response({'message': 'This is a protected view.'})
    
def issue_jwt(user, request):
    refresh = RefreshToken.for_user(user)
    request.session['jwt_refresh'] = str(refresh)
    request.session['jwt_access'] = str(refresh.access_token)
    print(f"Access + Refresh tokens were issued.")
    #jwt_refresh = request.session.get('jwt_refresh')
    #jwt_access = request.session.get('jwt_access')
    #print(f"Refresh Token issued: {jwt_refresh}")
    #print(f"Access Token issued: {jwt_access}")

class JWTAuthMixin:
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
                jwt_authenticator = JWTAuthentication()
                validated_token = jwt_authenticator.get_validated_token(token)
                request.user = jwt_authenticator.get_user(validated_token)
            except (InvalidToken, TokenError) as e:
                return JsonResponse({'error': str(e)}, status=401)
        else:
            return JsonResponse({'error': 'Authorization header missing'}, status=401)
        return super().dispatch(request, *args, **kwargs)
