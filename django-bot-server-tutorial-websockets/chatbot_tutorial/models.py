from django.db import models

# Create your models here.

class ChatbotModel(models.Model):
    vchr_user_name = models.CharField(max_length=50, blank=True, null=True)
    vchr_jock_type = models.CharField(max_length=10, blank=True, null=True)
