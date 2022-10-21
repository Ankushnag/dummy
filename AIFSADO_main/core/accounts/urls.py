from django.urls import path
from .import views

urlpatterns = [
    path('register/',views.UserRegistrationsView.as_view(),name='register'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',views.UserLogoutView.as_view(),name='logout'),
    path('profile/',views.UserProfileView.as_view(),name='profile'),
    path('changepassword/',views.UserChangePasswordView.as_view(),name='changepassword'),
    path('profileimage/',views.ChangeProfilePictureView.as_view(),name="profileimage"),
]
