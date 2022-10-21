from rest_framework import serializers
from .models import * 

# Registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    # pasword2 = serializers.CharField(style={"input_type":"password"},write_only=True)
    class Meta:
        model = User
        fields =["password","last_login","username","is_superuser","is_staff","is_active","date_joined",
        "email","is_email_verified"]
        extra_kwargs ={
            'pasword': {'write_only':True}
        }


    def create(self,validate_data):
        return User.objects.create_user(**validate_data)


# Login
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:  
        model=User
        fields ="__all__"


# Profile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


# Change Password
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=10, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=10, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password does not match")
        user.set_password(password)
        user.save()
        return attrs

class ChangeProfileImage(serializers.Serializer):
    image_url = serializers.ImageField(required=False)
    class Meta:
        model = UserProfile
        fields = ['id','user_type' 'profile_image']