#encoding:UTF-8
from django.db import models

# Create your models here.

class poem(models.Model):
	title = models.CharField(max_length=5000)
	writer = models.CharField(max_length=5000)
	content = models.CharField(max_length=5000) 
	

