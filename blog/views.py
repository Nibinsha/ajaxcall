from django.shortcuts import render
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


def index(request):
    if 'user' in request.session:
        return render(request, 'index.html', {'form': PostForm(),'class':ClassForm()})
    return HttpResponseRedirect('/login')


def homeone(request):

    return render(request, 'homeone.html',{})



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
                    request.session.set_expiry(200)
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