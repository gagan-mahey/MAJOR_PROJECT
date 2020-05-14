from django.db import models
from django.contrib.auth.models import User
import datetime

class Contact_Us(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=200)
    contact_number = models.IntegerField()
    message = models.TextField()

    class Meta:
        verbose_name_plural = "Contact_Us"

    def __str__(self):
        return self.name

class Category(models.Model):
    cat_name = models.CharField(max_length=250)
    cover_pic = models.FileField(upload_to="media/%Y/%m/%d")
    description = models.TextField()

    def __str__(self):
        return self.cat_name

class register_table(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)  
    contact_number = models.IntegerField()
    title = models.CharField(max_length=250,blank=True,null=True)
    profile_image = models.ImageField(upload_to="profiles",null=True,blank=True)
    about = models.TextField(blank=True,null=True)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Register Table"    



class add_property(models.Model):
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
    property_name = models.CharField(max_length=250)
    property_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    property_price = models.FloatField()
    sale_price = models.FloatField()
    property_image = models.ImageField(upload_to="products")
    details = models.TextField()

    def __str__(self):
        return self.property_name


