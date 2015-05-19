#coding=utf-8

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import re, sys, os
from django.db import connection
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from datetime import datetime, tzinfo, timedelta
import calendar
import pytz  
from django.contrib import auth


def index(request):
	template = loader.get_template('eatwhat/index.html')

	param = {}
	options = []

	if request.user.is_authenticated():
		param['user_logged_in'] = 'true'

	try:
		cursor = connection.cursor()
		cursor.execute("""
				SELECT a.course_id ,a.name, COUNT(b.vote_id) 
				FROM eatwhat_course a LEFT OUTER JOIN eatwhat_vote b
				ON a.course_id = b.course_id
				GROUP BY a.course_id
			""")

		options = cursor.fetchall()
	finally:
		cursor.close()

	param['options'] = options

	context = RequestContext(request, param)
	return HttpResponse(template.render(context))

@csrf_exempt
def djlogin(request):
	username = request.POST['username']
	password = request.POST['password']
	user = auth.authenticate(username=username, password=password)
	if user is not None and user.is_active:
		auth.login(request, user)
		return HttpResponse('@' + user.username)
	else:
		return HttpResponse('*')

@csrf_exempt
def djlogout(request):
	auth.logout(request)
	return HttpResponse('@')

@csrf_exempt
@transaction.atomic
def vote(request):
	if request.user.is_authenticated():
		courses = request.POST['courses'].split('*')[1:]

		try:
			cursor = connection.cursor()
			for course_id in courses:
				user_id = str(request.user.id)
				cursor.execute('INSERT INTO eatwhat_vote(course_id, user_id, date, status) VALUES (%s, %s, %s, %s)', [course_id, user_id, datetime.now().strftime('%Y-%m-%d'), str(1)])
		finally:
			cursor.close()

	return HttpResponse('ok')





