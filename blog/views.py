from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from .models import *
from .forms import *
from .serializers import PostSerializer
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_control
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
import stripe
import random
from django.core.mail import EmailMessage


def index(request):
    if 'user' in request.session:
        return render(request, 'index.html', {'form': PostForm(),'class':ClassForm()})
    return HttpResponseRedirect('/login')


def post_edit(request, pk):
    post = get_object_or_404(Class, pk=pk)
    if request.method == "POST":
        PostFormedit = PostFormEdit(request.POST, instance=post)
        ClassFormedit = ClassFormEdit(request.POST, instance=post)
        if PostFormedit.is_valid() and ClassFormedit.is_valid():
            postform = PostFormedit.save(commit=False)
            ClassFormedit = ClassFormedit.save(commit=False)

            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = ClassFormEdit(instance=post)
    return render(request, 'post_edit.html',{'clsData': PostFormEdit(), 'classForm': ClassFormEdit()})

def homeone(request):
    return render(request, 'homeone.html',{})

def sendingemail(request):
    generatedOtp = str(random.randint(1000, 10000))
    request.session["otp"] = generatedOtp
    message = render_to_string('sendmail.html', {
        'otp': generatedOtp
    })
    to_email = "nibinshanibi@gmail.com"
    email = EmailMessage(
        "otp check", message, to=[to_email]
    )
    email.send()
    return render(request, 'mailcheck.html')

@csrf_exempt
def checkotp(request):
    if request.method == "POST":
        a = request.body.decode('utf-8')
        body = json.loads(a)
        otp = body['otp']
        print(otp)
        sessionOtp = request.session['otp']
        print(sessionOtp)
        if otp == sessionOtp:
            return JsonResponse({'status': "success"})
        else:
            return JsonResponse({'status': "wrong"})
    return HttpResponseRedirect('/login')

def home(request):
    key = settings.STRIPE_PUBLISHABLE_KEY
    return render(request, 'home.html',{'key':key})


@csrf_exempt
def indexSave(request):
    if request.method == "POST" and 'user' in request.session:
        a = request.body.decode('utf-8')
        body = json.loads(a)
        post = Post()
        cls = Class()
        post.name = body['name']
        post.artist = body['artist']
        post.save()
        cls.student = body['student']
        cls.address = body['address']
        cls.save()
        return JsonResponse({'status': "success"})
    return HttpResponseRedirect('/login')


@api_view(['GET'])
def post_collection(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response({'data':serializer.data})

def login(request):
    loginform = LoginForm()
    Registrationform = RegistrationForm()
    return render(request, 'login.html', {'loginform':loginform,'Registrationform':Registrationform})


def fetchdata(request):
    if 'user' in request.session:
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response({'data': serializer.data})



@csrf_exempt
def registration(request):
    if request.method == "POST":
        a = request.body.decode('utf-8')
        body = json.loads(a)
        post = User()
        post.firstName = body['firstName']
        post.contactNo = body['contactNo']
        post.email = body['email']
        password = body['password']
        post.password = make_password(password)
        post.save()
    return JsonResponse({'status': "success"})

@csrf_exempt
def loggedin(request):
    if request.method == "POST":
        a = request.body.decode('utf-8')
        body = json.loads(a)
        email = body['email'].lower()
        password = body['pswd']
        if email and password:
            user = User.objects.get(email=email)
            if user is not None:
                if check_password(password, user.password):
                    request.session.set_expiry(2000)
                    request.session['user'] = user.userId
                    return JsonResponse({'status': "success"})
            return JsonResponse({'status': "wrong credentials"})
        else:
            return JsonResponse({'status': "wrong credentials"})
    loginform = LoginForm()
    Registrationform = RegistrationForm()
    return render(request, 'login.html', {'loginform': loginform, 'Registrationform': Registrationform})

@csrf_exempt
def logout(request):
   try:
      del request.session['user']
   except:
      pass
   return JsonResponse({'status': "success"})

@csrf_exempt
def charge(request): # new
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        charge = stripe.Charge.create(
            amount=500,
            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken'],
            metadata={'quantity': 2, 'order_id': 'A6735'},
        )
        return render(request, 'charge.html',{"charge":charge})

def postform(request):
    if 'user' in request.session:
         return render(request, 'postSave.html', {'form': PostForm(),'class':ClassForm()})


@csrf_exempt
def postSave(request):
    if request.method == "POST" and 'user' in request.session:
        a = request.body.decode('utf-8')
        body = json.loads(a)
        post = Post()
        cls = Class()
        post.name = body['name']
        post.artist = body['artist']
        post.save()
        cls.post = post
        cls.student = body['student']
        cls.address = body['address']
        cls.save()
        return JsonResponse({'status': "success"})
    return HttpResponseRedirect('/login')

def post_new(request):
    if request.method == 'POST':
       form = TestForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect('homeone')
    else:
       form = TestForm()
    return render(request, 'post_new.html', {'form': form})

def fetchData(request):
    data = Test.objects.all()
    return render(request, 'view_post.html', {'data': data})

def edit_post(request, pk):
    post = get_object_or_404(Test, pk=pk)
    if request.method == "POST":
        form = TestEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('fetchData')
    else:
        form = TestEditForm(instance=post)
    return render(request, 'post_new.html', {'form': form})

def fetchPostData(request):
    if 'user' in request.session:
        item = {}
        totalItems = []
        cls = Class.objects.all().values('student','address','post__name','post__artist','id')
        item['cls'] = list(cls)
        totalItems.append(item)
        return render(request,'savedData.html',{'data':list(cls),'postForm':PostFormEdit(),'classForm':ClassFormEdit()})
    return HttpResponseRedirect('/login')

def fetchpostDataViaId(request):
    if 'user' in request.session:
        a = request.body.decode('utf-8')
        body = json.loads(a)
        cls = Class.objects.filter(id=body['id']).values('student', 'address', 'post__name', 'post__artist')
        print(cls)
        return render(request, 'savedData.html',
                      {'data': list(cls), 'clsData': PostFormEdit(), 'classForm': ClassFormEdit()})
    return HttpResponseRedirect('/login')


