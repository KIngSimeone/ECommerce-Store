from django.db import models
from django.utils.timezone import now
from business.models import Business, Product
from account.models import User

class Order(models.Model):      
    business = models.ForeignKey(Business,on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
 
    createdAt = models.DateField("created_at", auto_now_add=True)

    def __str__(self):
        order = str(self.user) + " ordered " + str(self.products) + " from " + str(self.business) 
        return order