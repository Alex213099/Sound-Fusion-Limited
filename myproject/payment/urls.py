from . import views
from django.urls import path

urlpatterns=[
    path('stk_push',views.stk_push,name='stk_push'),
    path('mpesa_callback',views.mpesa_callback,name='mpesa_callback')
]