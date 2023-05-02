from django.db import models
from django.contrib.auth.models import User

# Plan model: Stores the plan details and the thumbnail heights
class Plan(models.Model):
    plan_name = models.CharField(max_length=100)
    thumbnail1_height = models.IntegerField(default=0)
    thumbnail2_height = models.IntegerField(default=0)
    original_link = models.BooleanField(default=False)
    expiring_link = models.BooleanField(default=False)

    def __str__(self):
        return self.plan_name


# Customer model: Stores the plan as foreign key and user details(one to one mapping with django user model)
class Customer(models.Model):
    plan = models.ForeignKey(Plan, default=1, on_delete=models.CASCADE)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

        
# Image model: Stores the image uploaded by the user
class Image(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='Test Image')
    uploaded_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='original_images/')
    thumbnail1 = models.CharField(max_length=100,default='')
    thumbnail2 = models.CharField(max_length=100, default='')
    original_link = models.CharField(default='', max_length=100)

    """
    Expiration link feature pending: Will be implemented by next week

    # expiration_link = models.CharField(default='', max_length=100)
    """
    