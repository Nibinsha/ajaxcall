from django.db import models

# Create your models here.

class User(models.Model):
    userId = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=30)
    contactNo = models.CharField(max_length=12)
    email = models.EmailField(max_length=60)
    password = models.CharField(max_length=100)

    def __int__(self):
        return self.userId


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    artist = models.CharField(max_length=255, null=False)
    def __str__(self):
        return self.name

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=255, null=False)
    def __str__(self):
        return self.student



