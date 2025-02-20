from django.urls import path
from . import views

urlpatterns =[
    path('',views.index,name="index"),
    path('signup',views.signup,name='signup'),
    path("login",views.login,name='login'), 
    path('dashboard', views.dashboard, name='dashboard'),  
    path('add_attendance',views.add_attendance,name='add_attendance'),
    path('list',views.list,name='list'),
    path('edit_attendance/<int:attendance_id>', views.edit_attendance, name='edit_attendance'),
]