from django.db import models

class Error(models.Model):
    code = models.TextField()
    description = models.TextField()

