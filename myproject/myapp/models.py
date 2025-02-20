from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,UserManager
from django.utils import timezone
from payment.models import Payment


# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("You have not provided a valid email adress")
        
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user( email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user( email, password, **extra_fields)



class User(AbstractBaseUser ,PermissionsMixin):
    email=models.EmailField(blank=True , default='',unique=True)
    name=models.CharField(max_length=255,blank=True,default='')
    phone_number=models.CharField(max_length=20)
    salary=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    gender=models.CharField(max_length=255,blank=True,default='none')
    date_of_Birth=models.DateField(null=True)
    disability=models.CharField(max_length=255,default='none')
    id_number=models.CharField(max_length=50, unique=True,null=True)


    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)

    date_joined=models.DateTimeField(default=timezone.now)
    last_login=models.DateTimeField(blank=True,null=True)

    objects=CustomUserManager()

    USERNAME_FIELD='email'
    EMAIL_FIELD='email'
    REQUIRED_FIELDS=[]

    class Meta:
        verbose_name='User'
        verbose_name_plural='Users'
    
    def get_full_name(self):
        return self.name


    def __str__(self):
        return self.email
    
class Event(models.Model):
    name=models.CharField(max_length=20)
    location=models.CharField(max_length=30)
    date=models.DateField()
    description=models.TextField(blank=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    hours_worked=models.PositiveIntegerField(default=8)
    overtime_hours=models.PositiveIntegerField(default=0)

    def calculate_pay(self,overtime_hours):
        base_pay=1000
        return (overtime_hours*100)+base_pay
    
    def save(self,*args,**kwargs):
        #check if attendance instace already exist (i.e its an update ,not an entry)
        if self.pk:
            old_attendace=Attendance.objects.get(pk=self.pk)#gets previous record
            old_overtime=old_attendace.overtime_hours#stores the old overtime

            if self.overtime_hours !=old_overtime:
                additional_pay=(self.overtime_hours-old_overtime)*100

                #update payment
                payment,created=Payment.objects.get_or_create(user=self.user)
                payment.Total_billed+=additional_pay#add the extra pay
                self.user.salary=payment.Total_billed
                payment.save()
                self.user.save()
        else:
            #if this is a new entry
            pay=self.calculate_pay(self.overtime_hours)
            payment,created=Payment.objects.get_or_create(user=self.user)
            payment.Total_billed+=pay
            self.user.salary=payment.Total_billed
            payment.save()
            self.user.save()
        super().save(*args,**kwargs)

    
    def __str__(self):
        return f"{self.user.name} - {self.event.name} - {self.date}"

