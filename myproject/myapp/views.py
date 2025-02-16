from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Payment

User=get_user_model()


# Create your views here.
def index(request):
    return render(request,'index.html',{'user':request.user})

def signup(request):
    if request.method=='POST':
        name=request.POST["name"]
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        phone_number=request.POST['phone_number']
        id_number=request.POST["id_number"]
        gender=request.POST['gender']
        date_of_Birth=request.POST['date_of_Birth']
        disability=request.POST['disability']

        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email is already in use")
                return redirect('signup')
            else:
                user=User.objects.create_user(disability=disability,date_of_Birth=date_of_Birth,gender=gender,email=email,password=password,name=name,phone_number=phone_number,id_number=id_number,)
                user.save()
                messages.success(request,"Created Successfully")
                return redirect('login')
        else:
            messages.info(request,"Password do not match")
            return redirect('signup')
    else:
        return render(request, 'signup.html')
    
def login(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("dashboard")
            messages.success(request,"Login Success")
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('login')
    else:
        return render(request,'login.html')
def dashboard(request):
    return render(request,"dashboard.html",{'User':User,'payment':Payment})