from django.urls import path

from . import views

urlpatterns=[
    path('index', views.index),
    path('homeone', views.homeone),
    path('indexSave', views.indexSave),
    path('posts', views.post_collection),
    path('post_collection', views.post_collection),
    path('login/', views.login),
    path('registration', views.registration),
    path('loggedin', views.loggedin),
    path('logout', views.logout),
    path('home', views.home),
    path('charge', views.charge, name='charge'),
    path('postform', views.postform, name='postform'),
    path('postSave', views.postSave, name='postSave'),
    path('fetchPostData', views.fetchPostData, name='fetchPostData'),
    path('fetchpostDataViaId', views.fetchpostDataViaId, name='fetchpostDataViaId'),
    path('sendingemail', views.sendingemail, name='sendingemail'),
    path('checkotp', views.checkotp, name='checkotp'),
    ]