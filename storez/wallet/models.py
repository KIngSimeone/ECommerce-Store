from django.db import models
from django.utils.timezone import now
from account.models import (
                            User,
                            Manager,
                            Controller
                            )
                            



# Create your models here.

class UserAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    balance = models.IntegerField(default=0)

    isDeleted = models.BooleanField("is_deleted", default= False)
    createdAt = models.DateField("created_at", auto_now_add=True)
    updatedAt = models.DateField("updated_at", auto_now=True)

    def __str__(self):
        account= str(self.user) + "'s Account"
        return account

class ManagerAccount(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)
    balance = models.IntegerField(default=0)

    isDeleted = models.BooleanField("is_deleted", default= False)
    createdAt = models.DateField("created_at", auto_now_add=True)
    updatedAt = models.DateField("updated_at", auto_now=True)

    def __str__(self):
        account= str(self.manager) + "'s Account"
        return account

class ControllerAccount(models.Model):
    controller = models.ForeignKey(Controller, on_delete= models.SET_NULL, null=True)
    balance = models.IntegerField(default=0)

    isDeleted = models.BooleanField("is_deleted", default= False)
    createdAt = models.DateField("created_at", auto_now_add=True)
    updatedAt = models.DateField("updated_at", auto_now=True)

    def __str__(self):
        account= str(self.manager) + "'s Account"
        return account