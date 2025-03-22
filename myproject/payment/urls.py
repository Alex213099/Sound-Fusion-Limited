from . import views
from django.urls import path

urlpatterns=[
    path('stk_push/<int:attendance_id>/',views.stk_push,name='stk_push'),
    path('mpesa_callback',views.mpesa_callback,name='mpesa_callback')
]