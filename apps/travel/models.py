# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class User_manager(models.Manager):
	def basic_validation(self, postData):
		errors = {}
		if len(postData['first_name']) < 2:
			errors["first_name"] = "first name should be at least 2 characters"
		if len(postData['last_name']) < 2:
			errors["last_name"] = "last name should be at least 2 characters"
		if not EMAIL_REGEX.match(postData['email']):
			errors["email"] = "email must match standard email format"
		if len(postData['password']) < 8:
			errors['password'] = "password needs to be at least 8 characters"
		return errors

class Trip_manager(models.Manager):
	def basic_validation(self, postData):
		errors = {}
		if len(postData['destination']) < 1:
			errors["destination"] = "Need to add a destination"
		if len(postData['description']) < 1:
			errors['description'] = "Need to add a description"
		return errors

class Users(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = User_manager()

class Trips(models.Model):
	destination = models.CharField(max_length=255)
	start_dt = models.DateTimeField()
	end_dt = models.DateTimeField()
	description = models.TextField()
	trip_creator = models.ForeignKey(Users, related_name="trips")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = Trip_manager()

class Travelers(models.Model):
	users = models.ForeignKey(Users, related_name="travelers")
	trips = models.ForeignKey(Trips, related_name="travelers")
	join_dt = models.DateTimeField(auto_now = True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)