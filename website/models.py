from djongo import models

# Create your models here.

class UserProjectDetails(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    service = models.CharField(max_length=100)
    details = models.TextField(max_length=500)
    datetime = models.DateTimeField(auto_now=True, auto_now_add=False)
