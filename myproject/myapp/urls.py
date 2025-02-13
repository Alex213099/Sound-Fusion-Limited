from django.urls import path
from . import views

urlpatterns =[
    path('',views.index,name="index"),
    path('',views.signup,name='signup'),
    path("login",views.login,name='login'),   
]