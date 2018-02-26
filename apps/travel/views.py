# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from models import *
# from datetime import datetime
import bcrypt

# Create your views here.
def login_page(request):
	return render(request, 'travel/login.html')

def trips_page(request):
	all_trips = Trips.objects.all()
	user_id = request.session['id']
	user_trips = Users.objects.get(id=user_id).trips.all()
	context = {
		'trips': all_trips,
		'user_trips': user_trips
	}
	return render(request, 'travel/main.html', context)

def add_destination_page(request):
	return render(request, 'travel/add_trip.html')

def add_destination(request):
	user_id = request.session['id']
	print (request.POST['start_dt'])
	dest = request.POST['destination']
	desc = request.POST['description']
	strt = request.POST['start_dt']
	end = request.POST['end_dt']
	Trips.objects.create(destination=dest, description=desc, start_dt=strt, end_dt=end, trip_creator=Users.objects.get(id=user_id))
	return redirect('/trips')

def trip_view(request, id):
	this_trip = Trips.objects.get(id=id)
	# people = Travelers.objects.get(trips=Trips.objects.get(id=1)).users#couldn't get it working :(
	context = {
	'trip': this_trip,
	# 'people': people
	}
	return render(request, 'travel/trip.html', context)

def trip_add(request, id):
	trip_id = id
	user_id = request.session['id']
	Travelers.objects.create(users=Users.objects.get(id=user_id), trips=Trips.objects.get(id=trip_id))
	return redirect('/destination/' + id)

def register(request):
	if request.method == "POST":
		errors = Users.objects.basic_validation(request.POST)
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
				return redirect('/')
		if request.POST['password'] != request.POST['password2']:
			messages.error(request, "Your passwords need to match")
			return redirect('/')
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		pw = request.POST['password']
		hash_pw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
		# password = request.POST['password']
		Users.objects.create(first_name=first_name, last_name=last_name, email=email,password=hash_pw)
		messages.error(request,"Registration accepted! Please log in")
		return redirect('/')
	else:
		return redirect('/')

def login(request):
	log_email = request.POST['log_email']
	log_passw = request.POST['log_password']
	query = Users.objects.filter(email=log_email)
	if len(query) != 0:
		stord_pw = query[0].password
		if bcrypt.checkpw(log_passw.encode(), stord_pw.encode()) == False:
			messages.error(request, "It appears you entered your password incorrectly")
			return redirect('/')
		else:
			#session log in
			request.session['id'] = query[0].id
			# print ('session id is ' + str(request.session['id']))#for testing purposes
			messages.error(request,"session log in")
			return redirect('/trips')
	else:
		messages.error(request, "Cannot find your account.")
		return redirect('/')

def log_out(request):
	#session log out
	request.session.clear()
	# messages.clear()
	return redirect('/')