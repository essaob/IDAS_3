
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.test import TestCase
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,User

# class CustomUser(AbstractUser):
#     is_investor = models.BooleanField(default=False)
#     mailing_address = models.CharField(max_length=200, blank=True)



class User(AbstractBaseUser):
    INVESTOR = 1
    ADMIN = 2
    ROLE_CHOICES = (
        (INVESTOR, 'Investor'),
        (ADMIN, 'Admin')
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=False, null=False)


class ContactUsModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=500)

    def __str__(self):
        return self.email


class ContactAdmin(models.Model):
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=500)

    def __str__(self):  # func to see email inthe tasks list
        return self.subject



# class CustomUser(AbstractUser):
#     is_student = models.BooleanField(default=False)
#     is_investor = models.BooleanField(default=False)
#     mailing_address = models.CharField(max_length=200, blank=True)
#     college = models.CharField(max_length=30)
#     major = models.CharField(max_length=30)

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='portfolio/images/')
    url = models.URLField(blank=True)
    # user = models.ForeignKey(CustomUser,
    #               on_delete=models.CASCADE)  # key that connect user and project that he created (import: from django.contrib.auth.models import User)

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(Project, self).delete(*args, **kwargs)
        storage.delete(path)

    def __str__(self):
        return self.title
