from django.urls import path,include
from accounts.views import *

urlpatterns = [
    
    path('createuser',UserRegistration.as_view(),name='createuser'),
    path('updateuser/<int:id>',UpdateCustomeUser.as_view(),name='updateuser'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    
    
     
    #user login and Logout
    path('user_login', UserLogin.as_view(), name='user_login'),
    path('userlogout', UserLogout.as_view(), name='userlogout'),
    path('api/changepassword', ChangePassword.as_view(), name='api/changepassword'),
    

]
