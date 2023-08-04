from django.db import models
import uuid
# Create your models here.

class Account(models.Model):
    email = models.EmailField(unique=True)
    acc_id = models.CharField(max_length=100, unique=True)
    acc_name = models.CharField(max_length=100)
    app_token = models.CharField(max_length=100, unique=True)
    website = models.URLField(blank=True, null=True)

class Destination(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='destinations')
    url = models.URLField()
    http_method = models.CharField(max_length=10)  # 'GET', 'POST', 'PUT'
    headers = models.JSONField()

class DataHandler(models.Model):
    data_id = models.CharField(primary_key=True, default=False, editable=False, max_length=10)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='data_handlers')
    data = models.JSONField()