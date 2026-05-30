from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .. import services
from ..serializers.serializers import (
  RegisterSerializer
)


           
            
## User 

class RegisterApi(APIView):
    """
    Route: /api/auth/register/
    """
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            services.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data.get('email',''),
                password=serializer.validated_data['password']
                )
            return Response({"detail":"Register successfully"},status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    
class LogoutApi(APIView):
    """
    Route: /api/auth/logout/
    """
    def post(self,request):
       try:
           refresh_token = request.data.get('refresh')
           if not refresh_token:
              return Response({"detail":"Refresh token is mandatory"}, status=status.HTTP_400_BAD_REQUEST)
          
           token = RefreshToken(refresh_token)
           token.blacklist()
           
           return Response({"detail":"Logout successfully"},status=status.HTTP_205_RESET_CONTENT)
       
       except Exception:
           return Response({"detail":"Invalid token:"},status=status.HTTP_400_BAD_REQUEST)   
    
        