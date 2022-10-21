from django.db import models
from accounts.models import *


class Property_Main_Category(models.Model):
    Category_name = models.CharField(max_length = 255)
    is_active = models.BooleanField(default=False)

class Property_Sub_Category(models.Model):
    property_main_category = models.ForeignKey(to = Property_Main_Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

class Property_Type(models.Model):
    property_sub_category = models.ForeignKey(to = Property_Sub_Category, on_delete=models.CASCADE)
    proprty_type_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)

class Amenities_Master(models.Model):
    amenities_icon = models.ImageField(upload_to='Amenities_icon')
    amenities_name = models.CharField(max_length = 255)
    amenities_type = models.IntegerField()
    is_active = models.BooleanField(default=False)

class Property_Detail(models.Model):
    property_title = models.CharField(max_length=255)
    propert_description = models.TextField()
    property_main_image = models.ImageField(upload_to='Property_main_image')
    property_main_floor_plan = models.ImageField(upload_to='Property_main_floor_plan')
    property_sub_category = models.ForeignKey(to = Property_Sub_Category, on_delete=models.CASCADE)
    property_type = models.ForeignKey(to = Property_Type, on_delete=models.CASCADE)
    property_address_1 = models.TextField()
    property_address_2 = models.TextField()
    property_town = models.CharField(max_length=100)
    property_state = models.CharField(max_length=100)
    property_zip = models.CharField(max_length=10)
    property_terms = models.CharField(max_length=100)
    property_offer = models.CharField(max_length=100)
    is_property_fee = models.BooleanField(default=False)
    property_fee = models.CharField(max_length=50, null=True)
    property_listing_amount = models.IntegerField()
    created_date_time = models.DateTimeField()
    user_profile = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)

class Property_Amenities(models.Model):
    ameniites_master = models.ForeignKey(to= Amenities_Master, on_delete = models.CASCADE)
    property_details = models.ForeignKey(to=Property_Detail, on_delete= models.CASCADE)
    amenities_value = models.CharField(max_length=255)
    created_date = models.DateTimeField()

class Property_listing_event(models.Model):
    property_details = models.ForeignKey(to=Property_Detail, on_delete=models.CASCADE)
    is_property_exclusive = models.BooleanField(default=False)
    property_listing_start_date = models.DateTimeField()
    property_listing_end_date = models.DateTimeField()