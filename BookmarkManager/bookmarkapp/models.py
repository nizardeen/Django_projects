from django.db import models

class Customer(models.Model):
	Latitude = models.FloatField(null=True,blank=True)
	Longitude = models.FloatField(null=True,blank=True)


class Bookmark(models.Model):
	Customer = models.ManyToManyField(Customer)
	Title = models.CharField(max_length=250,blank=True,null=True)
	Url = models.CharField(max_length=250,blank=True,null=True)
	Source_Name = models.CharField(max_length=250,blank=True,null=True)
	Date = models.DateField(auto_now_add = True,blank=True,null=True)
	
		



