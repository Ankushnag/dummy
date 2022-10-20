from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import json
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.core import serializers as core_serializers
from django.views.decorators.csrf import csrf_exempt
from .renderers import *
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# generating token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
  

# Registration
class UserRegistrationsView(APIView):
    def post(self,request,format=None): 
        body = request.data
        if 'password' in body and 'password2' in body and 'user_type' in body:
                if body['password'] == body['password2']:
                    print('yes')
                    del body['password2']
                    print(body)

                    serializer = UserRegistrationSerializer(data = body)

                    if serializer.is_valid(raise_exception = True):   #remove the the raise_exception = True
                        user = serializer.save()
                        UserType.objects.create(user=user,user_type=body['user_type'])
                        return Response({'msg':'Registration Sucess'},
                        status = status.HTTP_201_CREATED)
                        # after the remove the raise_exceptions = True then the that place print(serializer.errors)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
                else:
                    return Response({'Password Not Matched'})
        else:
            return Response({'msg':'password, password2, user_type is Required'})
    


# login 
class UserLoginView(APIView):
    def post(self,request,format=None):
        obj=request.data
        if 'username' in obj and 'password' in obj:
            if User.objects.filter(username=obj['username']):
                user_object=User.objects.get(username=obj['username'])
                user=authenticate(username=user_object.username,password=obj['password'])
                if user is not None:
                    token = get_tokens_for_user(user)
                    login(request, user)
                    serializer=UserLoginSerializer(user)
                    usertypeobj=UserType.objects.get(user=user)
                    print('Login Successfully')
                    return Response({'user_info':{'id':user.id,'username':user.username,'usertypeobj':usertypeobj.user_type},'token':token,'msg':'login Success'}, status = status.HTTP_200_OK)
                else:
                    return Response({'msg : Credentials Not Matched'})
            return Response({'detail : No active accout found with given credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message : username and password needed'}, status=status.HTTP_400_BAD_REQUEST)


        

class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            print(request.data)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        # except Exception as e:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

# profile
class UserProfileView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format = None):
        serializer = UserProfileSerializer(request.user)
        # if serializer.is_valid(raise_exception = True):
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self,request):
        body=request.data
        


# change Password
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format = None):
        serializer = UserChangePasswordSerializer(data = request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception = True):
            return Response({'msg':'Password Change Sucessfully'}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)