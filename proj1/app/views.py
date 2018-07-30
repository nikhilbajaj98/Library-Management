# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect

from models import *

from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q

import random

from django.core.mail import send_mail

from datetime import date

from datetime import timedelta

from django.http import HttpResponse

from reportlab.pdfgen import canvas

from io import BytesIO

# Create your views here.

@csrf_exempt
def start(request):
	if 'username' in request.session:
		obj=User.objects.get(username=request.session['username'])
		if obj.user_type=='student':
			return redirect('/stu/')
		else:
			return redirect('/lib/')
	else:
		return redirect('/login/')
@csrf_exempt
def register(request):
	if request.method=='GET':
		return render(request,'reg.html',{})
	elif request.method=='POST':	
		context={}
		name=request.POST['name']
		username=request.POST['username']
		password=request.POST['password']
		email=request.POST['email']
		phone_number=request.POST['phone_number']
		user_type=request.POST['user_type']
		if User.objects.filter(username=username).exists():
			context['message']='Username Already Exists'
			return render(request,'reg.html',context)
		else:
			abc=User( name=name,
				  username=username,
				  password=password,
				  email=email,
				  phone_number=phone_number,
				  user_type=user_type,
				  )
			abc.save()
			'''context['name']=name
			context['username']=username
			context['password']=password
			context['email']=email
			context['phone_number']=phone_number
			context['user_type']=user_type'''
	return render(request,'login.html',context)

	
@csrf_exempt
def login(request):
	if 'username' in request.session:
		if request.session['access'] == 'librarian':
			return redirect('/lib')
		elif request.session['access'] == 'student':
			return redirect ('/stu/')

	if request.method=='GET':
		
		return render(request,'login.html',{})
	elif request.method=='POST':
		context={}
		username=request.POST['username']
		password=request.POST['password']
		if User.objects.filter(username=username).exists():
			user_obj=User.objects.get(username=username)
			print 'abc'
			if user_obj.password==password:
				request.session['username']=user_obj.username
				request.session['access']=user_obj.user_type	
				if user_obj.user_type == 'librarian':
					print 'librarian'
					return redirect('/lib/')
				elif user_obj.user_type =='student':
					print 'student'
					return redirect('/stu/')
			else:
				context['message']='Wrong password'
				return render(request,'login.html',context)
		else:
			context['message']='Username does not exist'
			return render(request,'reg.html',context)
				



def student(request):
	context={}
	if 'username' in request.session:
		obj=Book.objects.all()
		context['books']=obj
		return render(request,'stu.html',context)
	else :
		return redirect('/login/')
 

def librarian(request):
	context={}
	return_list = BookIssue.objects.filter(BookStatus='booked')
	return_date_list = []
	for i in return_list:
		return_dict = {}
		return_dict['BookName'] = i.BookName.Name
		return_dict['StudentName'] = i.StudentName.username
		return_dict['BookStatus'] = i.BookStatus
		return_dict['IssueDate'] = i.IssueDate
		return_dict['ReturnDate'] = i.IssueDate + timedelta(days=7)
		print return_dict['ReturnDate']
		return_date_list.append(return_dict)
	context['issue'] = return_date_list

	return_list = BookIssue.objects.filter(BookStatus='pickedUp')
	return_date_list = []
	print return_list
	for i in return_list:
		return_dict = {}
		return_dict['BookName'] = i.BookName.Name
		return_dict['StudentName'] = i.StudentName.username
		return_dict['BookStatus'] = i.BookStatus
		return_dict['IssueDate'] = i.IssueDate
		return_dict['ReturnDate'] = i.IssueDate + timedelta(days=7)
		days_left = (i.IssueDate + timedelta(days=7)) - date.today()
		days_left = str(days_left)
		a = days_left.split(' ')
		return_dict['DaysLeft'] = a[0]
		request.session['DaysLeft'] = return_dict['DaysLeft'] 
		return_date_list.append(return_dict)
	context['issue2'] = return_date_list


	# obj = BookIssue.objects.filter(BookStatus ='booked')
	# context['issue'] = obj

	# obj1 = BookIssue.objects.filter(BookStatus = 'pickedUp')
	# obj1.order_by('DaysLeft')
	# for i in obj1:
	# 	i.DaysLeft = i.ReturnDate - date.today()
	# 	i.DaysLeft = str(i.DaysLeft)
	# 	a=i.DaysLeft.split(' ')
	# 	i.DaysLeft = a[0]
	# context['issue2'] = obj1
	return render(request,'lib.html',context)

def logout(request):
	if 'username' in request.session:
		del request.session['username']
		del request.session['access']
	return redirect('/login/')

def summary(request):
	context={}
	id1=request.GET['book_id']
	request.session['bookid']=id1
	obj=Book.objects.get(id=id1)
	context={'Name':obj.Name,'Author':obj.Author,'Subject':obj.Subject,'Rating':obj.Rating,'Summary':obj.Summary,'No_of_Copies':obj.No_of_Copies,}
	return render (request,'book_details.html',context)

def profile(request):
	context={}
	if 'username' in request.session:
		u=request.session['username']
		obj1=User.objects.get(username=u)
		context={'Username':obj1.username,'Name':obj1.name,'Email':obj1.email,'phone':obj1.phone_number,'Type':obj1.user_type}
		return render(request,'profile.html',context)
	else:
		context['message']='Log in to view profile'
		return render(request,'login.html',context)
@csrf_exempt
def results(request):
	context={}
	obj=Book.objects.filter(Q(Name=request.POST['Title']) | Q(Author=request.POST['Title']) | Q(Subject=request.POST['Title']))
	context['books']=obj
	return render(request,'results.html',context)

def lostpass(request):
	return redirect('/verify/')

@csrf_exempt
def verify(request):
	context={}
	if request.method=='GET':
		return render(request,'verify.html',{})
	elif request.method=='POST':
		email=request.POST['mailid']
		print email
		verification_code=random.randint(100000,199999)
		verification_code=str(verification_code)
		print verification_code
		request.session['code']=verification_code
		request.session['email']=email
		send_mail('Password Reset',verification_code,'nbajaj201@gmail.com',[email])
		return render(request,'verify1.html',context)
@csrf_exempt
def verify1(request):
	context={}
	if request.method=='GET':
		return render(request,'verify1.html',{})
	elif request.method=="POST":
		code=request.session['code']
		entered_code=request.POST['vcode']
		if code==entered_code:
			return redirect('/change/')
		else:
			context['message']='Wrong Verification Code'
			return render(request,'verify1.html',context)
@csrf_exempt
def change(request):
	if request.method=="GET":
		return render(request,'change.html',{})
	elif request.method=="POST":
		password=request.POST['npass']
		email=request.session['email']
		obj=User.objects.get(email=email)
		obj.password=password
		obj.save()
		return render(request,'change.html',{})

	
@csrf_exempt
def reqbook(request):
	id1=request.session['bookid']
	obj=Book.objects.get(id=id1)
	name = request.session['username']
	obj1 = User.objects.get(username=name)
	context={'Name':obj.Name,'Author':obj.Author,'Subject':obj.Subject,'Rating':obj.Rating,'Summary':obj.Summary,'No_of_Copies':obj.No_of_Copies,}
	if BookIssue.objects.filter(Q(StudentName__username=request.session['username']) & Q(Q(BookStatus='booked') | Q(BookStatus='pickedUp'))).exists():
		context['message'] = 'Issue Suspended,Return Previous Issued Books to Issue a New One!'
		return render(request,'book_details.html',context)
		

	else:
		abc=BookIssue(
					BookName = obj,
					StudentName = obj1,
					BookStatus  = 'booked',
					IssueDate = date.today(),
					)
		abc.save()

		# obj1 = BookIssue.objects.get(StudentName=name)
		# xyz = StudentHistory(
		# 			StudentName = obj1.StudentName,
		# 			BookName = obj1.BookName,
		# 			BookStatus = obj1.BookStatus,
		# 			IssueDate = date.today()
		# 	)
		# xyz.save()
		obj.No_of_Copies -= 1
		obj.save()
		context={'Name':obj.Name,'Author':obj.Author,'Subject':obj.Subject,'Rating':obj.Rating,'Summary':obj.Summary,'No_of_Copies':obj.No_of_Copies,}
		context['message']='Book Granted!'

		return render(request,'book_details.html',context)


@csrf_exempt
def history(request):
	context={}
	obj = BookIssue.objects.filter(StudentName__username = request.session['username'])
	context['history'] =obj
	return render(request,'History.html',context)	

@csrf_exempt
def pickedup(request):
	name = request.GET['name']
	obj = BookIssue.objects.get(Q(StudentName__username=name) & Q(BookStatus='booked'))
	obj.BookStatus = 'pickedUp'
	obj.save()
	return redirect('/lib/')

@csrf_exempt
def Return(request):
	name = request.GET['name']
	obj = BookIssue.objects.get(Q(StudentName__username=name) & Q(BookStatus='pickedUp'))
	DaysLeft = int(request.session['DaysLeft']) 
	if 'DaysLeft' in request.session:
		del request.session['DaysLeft']
	if DaysLeft<0:
		generateBill(DaysLeft)
	obj.BookStatus = 'returned'
	obj.save()
	obj1 = Book.objects.get(Name=obj.BookName)
	obj1.No_of_Copies += 1
	obj1.save()
	return redirect('/lib/')


def generateBill(DaysLeft):
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="LateFee.pdf"'
		# Create the PDF object, using the response object as its "file."
		p = canvas.Canvas(response)
		# Draw things on the PDF. Here's where the PDF generation happens.
		# See the ReportLab documentation for the full list of functionality.
		print 'inside '
		buffer = BytesIO()
		print "Late Fee: Rs"+str(50*abs(DaysLeft))
		p.drawString(100, 100, "Late Fee: Rs"+str(50*abs(DaysLeft)))
		# Close the PDF object cleanly, and we're done.
		p.showPage()
		p.save()
		response.write(p)
		return response

		#abcd