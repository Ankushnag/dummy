from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from macaddress.fields import MACAddressField
from PIL import Image

class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False)

class UserType(models.Model):
    user=models.OneToOneField(to=User,on_delete=models.SET_NULL, null=True)
    user_type=models.IntegerField()

class UserProfile(models.Model):
    user_type=models.OneToOneField(unique=True,to=UserType,on_delete=models.SET_NULL,null=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    work_number_1=models.CharField(max_length=10)
    work_number_2=models.CharField(max_length=10,null=True)
    cell_number=models.CharField(max_length=10,null=True)
    is_work_numer_1_valid=models.BooleanField(default=False)
    type_of_account=models.IntegerField(null=True)
    profile_image=models.ImageField(upload_to='profile_pictures',null=True)
    brokerage_name=models.CharField(max_length=100,null=True)
    sales_persones_license=models.CharField(max_length=100,null=True)
    agent_broker_license_title=models.CharField(max_length=100,null=True)
    create_team=models.BooleanField(null=True)
    team_name=models.CharField(max_length=50,null=True)
    languages=models.JSONField(null=True)
    linkedin_url=models.URLField(max_length=200,null=True)
    twitter_url=models.URLField(max_length=200,null=True)
    favebook_url=models.URLField(max_length=200,null=True)
    instagram_url=models.URLField(max_length=200,null=True)
    youtube=models.URLField(max_length=200,null=True)
    personal_bio=RichTextField(null=True)
    is_profilepassword=models.BooleanField(null=True)
    profile_password=models.CharField(max_length=10,null=True)
    name_of_business_listing=models.CharField(max_length=100, null=True)
    business_id=models.CharField(max_length=50,null=True)
    addition_user=models.CharField(max_length=50, null=True)
    number_user=models.IntegerField(null=True)
    address_line_1=models.CharField(max_length=100, null=True)
    address_line_2=models.CharField(max_length=100, null=True)
    town_id=models.CharField(max_length=100)
    state_id=models.CharField(max_length=100)
    zip_code_id=models.CharField(max_length=6)

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        super().save()  # saving image first
        img = Image.open(self.profile_image.path) # Open image using self
        if img.height > 1080 or img.width > 1080:
            new_img = (1080,1080)
            img.thumbnail(new_img)
            img.save(self.profile_image.path)  # saving image at the same path


class User_Log(models.Model):
    user_type = models.ForeignKey(to=UserType, on_delete=models.CASCADE)
    action_type = models.BooleanField(default=False)
    date_time = models.DateTimeField()
    ip_address = models.GenericIPAddressField()
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    mac_address = MACAddressField()
    location = models.TextField()