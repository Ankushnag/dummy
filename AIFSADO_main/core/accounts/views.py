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
from rest_framework.parsers import MultiPartParser, FormParser
import os
import uuid

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
        if 'username' in obj and 'password' in obj and 'user_log' in obj:
            if 'action_type' in obj['user_log'] and 'date_time' in obj['user_log'] and 'ip_address' in obj['user_log'] and 'longitude' in obj['user_log'] and 'latitude' in obj['user_log'] and 'mac_address' in obj['user_log'] and 'location' in obj['user_log'] :
                if User.objects.filter(username=obj['username']):
                    user_object=User.objects.get(username=obj['username'])
                    user=authenticate(username=user_object.username,password=obj['password'])
                    if user is not None:
                        token = get_tokens_for_user(user)
                        login(request, user)
                        usertypeobj=UserType.objects.get(user=user)
                        User_Log.objects.create(user_type=usertypeobj,action_type=obj['user_log']['action_type'],
                        date_time=obj['user_log']['date_time'],ip_address=obj['user_log']['ip_address'],
                        longitude=obj['user_log']['longitude'],latitude=obj['user_log']['latitude'],
                        mac_address=obj['user_log']['mac_address'],location=obj['user_log']['location'])
                        return Response({'user_info':{'id':user.id,'username':user.username,'usertypeobj':usertypeobj.user_type},'token':token,'msg':'login Success'}, status = status.HTTP_200_OK)
                    else:
                        return Response({'msg : Credentials Not Matched'})
                return Response({'detail : No active accout found with given credentials'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message : action_type, date_time, ip_address, longitude, latitude, mac_address, location needed '}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message : username and password and user_log needed'}, status=status.HTTP_400_BAD_REQUEST)


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
        user = request.user
        usertypeobj=UserType.objects.get(user=user)
        body=request.data
        if 'first_name' in body and 'last_name' in body and 'phone_number' in body and 'type_of_account' in body and 'town' in body and 'state' in body and 'zipcode' in body:
            if UserProfile.objects.filter(work_number_1=body['phone_number']):
                return Response({'meg':"this Phone number is alreay taken"})
            else:
                UserProfile.objects.create(
                    user_type=usertypeobj, first_name=body['first_name'], last_name=body['last_name'], work_number_1=body['phone_number'], 
                    type_of_account=body['type_of_account'], town_id=body['town'], state_id=body['state'], zip_code_id=body['zipcode'],
                )
                return Response({'meg':"success"})
        else:
            return Response({'meg':"first_name, last_name, phone_number, type_of_account, town, state, zipcode needed "})



# change Password
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format = None):
        serializer = UserChangePasswordSerializer(data = request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception = True):
            return Response({'msg':'Password Change Sucessfully'}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeProfilePictureView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def put(self, request, format = None):
        user= request.user
        usertypeobj=UserType.objects.get(user=user)
        if request.FILES.get("image", None) is not None:
                img = request.FILES["image"]
                if UserProfile.objects.filter(user_type=usertypeobj):
                    userprofileobj=UserProfile.objects.get(user_type=usertypeobj)
                else:
                    return Response({'msg':"UserProfile id is invalid"})
                userprofileobj.profile_image=img
                userprofileobj.save()
                return Response({'msg':"profile image updated"})
        else:   
                return Response({'msg':"Profile image not found"})
        

            
            
        
        