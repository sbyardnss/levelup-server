from django.db import models

class Gametype(models.Model):
    """django gametype instance"""
    label = models.CharField(max_length=50)