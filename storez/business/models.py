from django.db import models
from django.utils.timezone import now
from account.models import User

class Business(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    businessName = models.TextField(max_length=254)
    businessEmail = models.EmailField(max_length=254)
    businessPhone = models.TextField()

    isDeleted = models.BooleanField("is_deleted", default=False)
    createdAt = models.DateField("created_at", auto_now_add=True)
    
    def __str__(self):
        name = self.businessName
        return name

class BusinessAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    business = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True)
    street = models.TextField(null=False)
    city = models.CharField(max_length=64, null=False)
    state = models.CharField(max_length=64, null=False)
    country = models.CharField(max_length=64, null=False)
    zipCode = models.CharField(max_length=64, null=False)

    def __str__(self):
        address = str(self.business) + "'s Address"
        return address


class Product(models.Model):
    business = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True)
    productName = models.TextField(max_length=254)
    productPrice = models.FloatField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        name = str(self.productName)
        return name



class Photo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) 
    title = models.CharField(max_length=100)
    photo = models.FileField()