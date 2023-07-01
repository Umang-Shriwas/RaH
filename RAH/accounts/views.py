from django.shortcuts import render
from accounts.models import MultiToken
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import *
from django.contrib.auth import authenticate, login, logout
from accounts.authentication import MultiTokenAuthentication, MultiToken
from rest_framework.permissions import IsAuthenticated

class UserRegistration(CreateAPIView):
    # parser_classes = (MultiPartParser, FormParser)
    def post(self,request):
        customuser = CustomUserCreationSerializer(data=request.data)
        if customuser.is_valid():
           customuser.save()
           return Response(customuser.data,status=status.HTTP_201_CREATED) 
        else:
            return Response(customuser.errors,status=status.HTTP_400_BAD_REQUEST)  

        
class UpdateCustomeUser(APIView):
     def put(self,request,id):
        res = CustomUser.objects.get(id=id)
        user = UpdateUserSerializer(res,request.data,partial=True)
        if user.is_valid():
           user.save()
           return Response(user.data,status=status.HTTP_200_OK) 
        else:
            return Response(user.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
class UserLogin(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        try:
            print(email,password)
            user = authenticate(request,email=email,password=password)
            if user:
                login(request,user)
                token = MultiToken.objects.create(user=user)
                ser = CustomUserSerializer(user)
                # print("Token",token)
                context = {
                    "data":ser.data,
                    "token":token.key,
                }
                return Response(context,status=status.HTTP_202_ACCEPTED)
            else:
                message = {"message":"Invalid Credential"}
                return Response(message,status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            message = {"message":"Invalid Credential"}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        

class UserLogout(APIView):
    authentication_classes = [MultiTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        MultiToken.objects.get(user=request.user,key=request.data['key']).delete()
        logout(request)
        message = {"message":"logout successfully"}
        return Response(message,status=status.HTTP_200_OK)
    
    
class ChangePassword(APIView):
    authentication_classes = [MultiTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, 
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            message = {"message":"Password Changed Successfully"}
            return Response(message,status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)