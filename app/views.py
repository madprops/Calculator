import os
import json
import random
import string
import datetime
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from app.models import *

root = os.path.dirname(os.path.dirname(__file__))

html_escape_table = {
	"&": "&amp;",
	'"': "\&quot;",
	"'": "&#39;",
	">": "&gt;",
	"<": "\&lt;",
	}

html_escape_table2 = {
	"&": "&amp;",
	'"': "&quot;",
	"'": "&#39;",
	">": "&gt;",
	"<": "&lt;",
	}

def html_escape(text):
	return "".join(html_escape_table.get(c,c) for c in text)
	
def html_escape2(text):
	return "".join(html_escape_table2.get(c,c) for c in text)

def log(s):
	with open(root + '/log', 'a') as log:
		log.write(str(s) + '\n\n')

def random_alpha(n):
	return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(n))

def now():
	return datetime.datetime.now()

@csrf_protect
def main(request):

	if request.method == 'POST':
		pass

	c = {}

	c['content'] = ''

	return render(request, 'index.html', c)

@csrf_protect
def load_sheet(request, uid):

	try:
		sheet = Sheet.objects.get(uid=uid)
	except:
		return HttpResponseRedirect('/')

	c = {}

	c['content'] = sheet.content

	return render(request, 'index.html', c)

@csrf_protect
def save_sheet(request):

	if request.method == 'POST':

		content = request.POST.get('content', '')

		data = {'response':'nothing'}

		if len(content.strip()) < 1:
			data['response'] = 'empty'

		elif len(content) > 50000:
			data['response'] = 'toobig'

		else:
			sheet = Sheet(content=content, date=now())
			sheet.uid = random_alpha(8)
			success = False
			failures = 0

			while not success:
				try:
					sheet.save()
				except IntegrityError:
					failures += 1
					if failures > 10:
						raise
					else:
						sheet.uid = random_alpha(9)
				else:
					success = True

			data['response'] = sheet.uid

		return HttpResponse(json.dumps(data), content_type="application/json")
			

