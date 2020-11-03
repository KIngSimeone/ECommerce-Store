from django.db import models
from account.models import User
from django.utils.timezone import now
from business.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateField("created_at", auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()

    def __str__(self):
        cart = str(self.user) + "-" + str(self.product)


        