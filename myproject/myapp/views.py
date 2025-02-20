from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Payment
from .form import AttendanceForm
from datetime import date
from .models import Attendance
from django.contrib.auth.decorators import login_required
from payment.models import Payment


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

def login(request,):
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
    
@login_required
def dashboard(request):
    payment,create=Payment.objects.get_or_create(user=request.user)
    user=request.user
    if payment:
        payment.refresh_from_db()
    if user:
        user.refresh_from_db()

    return render(request,"dashboard.html",{'user':user,'payment':payment})
@login_required
def add_attendance(request):
    attendance=None
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        print(request.user)
        if form.is_valid():
            attendance = form.save(commit=False)  # Don't save yet
            attendance.user = request.user # Assign the logged-in user
            attendance.date = date.today()  # Set the date
            attendance.save()
            return redirect('list')
        else:
            print("Form errors:", form.errors)  # Debugging
            

    else:
        attendance = Attendance.objects.filter(user=request.user, date=date.today()).first()
        form = AttendanceForm(instance=attendance) if attendance else AttendanceForm()

    return render(request, 'add_attendance.html', {'form': form,'attendance':attendance})
@login_required
def edit_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id, user=request.user)
    
    if request.method == "POST":
        # Get new values from the form
        old_overtime = attendance.overtime_hours  # Store old overtime value
        new_overtime = int(request.POST.get("overtime_hours", 0))
        
        # Check if overtime hours changed
        if old_overtime != new_overtime:
            additional_pay = (new_overtime - old_overtime) * 100

            # Update the user's payment record
            payment, created = Payment.objects.get_or_create(user=request.user)
            payment.Total_billed += additional_pay
            request.user.salary = payment.Total_billed
            payment.save()

        # Update attendance details
        attendance.hours_worked = request.POST.get("hours_worked", 8)  # Default to 8 if empty
        attendance.overtime_hours = new_overtime
        attendance.save()
        
        return redirect("dashboard")  # Redirect after saving

    return render(request, "edit_attendance.html", {"attendance": attendance})
@login_required
def list(request):
    attendants=Attendance.objects.all()


    return render(request,'list.html',{'attendants':attendants})