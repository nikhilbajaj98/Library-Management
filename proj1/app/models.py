# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
user_type = (
		('librarian','LIBRARIAN'),
		('student','STUDENT'),
		)
class User(models.Model):
	name = models.CharField(max_length=50)
	username = models.CharField(max_length=50,blank=False)
	password = models.CharField(max_length=50,blank=False)
	email = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=50)
	user_type=models.CharField(max_length=50,choices=user_type,default='student')

	def __str__(self):
		return self.name 

class Book(models.Model):
	Name=models.CharField(max_length=50)
	Author=models.CharField(max_length=50)
	Subject=models.CharField(max_length=50)
	Rating=models.CharField(max_length=50)
	Summary=models.CharField(max_length=500)
	No_of_Copies=models.IntegerField()
	No_of_Requests=models.IntegerField()

	def __str__(self):
		return self.Name

bookstatus=(('booked','BOOKED'),
			('pickedUp','PICKED_UP'),
			('returned','RETURNED'),
		)
class BookIssue(models.Model):
	BookName=models.ForeignKey(Book)
	StudentName=models.ForeignKey(User)
	BookStatus=models.CharField(max_length=50,choices=bookstatus,default='returned')
	IssueDate=models.DateField(null=True)
	DaysLeft = models.IntegerField()

	def __str__(self):
		return self.BookName.Name

