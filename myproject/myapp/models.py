from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    phone_number=models.CharField(max_length=20)
    salary=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.username
    
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
    overtime_hours=models.PositiveIntegerField(default=8)

    def calculate_pay(self,overtime_hours):
        base_pay=1000
        return (overtime_hours*100)+base_pay
    def __str__(self):
        return f"{self.user.username} - {self.event.name} - {self.date}"

class Payment(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    total_paid=models.DecimalField(max_digits=10,decimal_places=2 ,default=0.00)
    last_payment_date=models.DateField(auto_now_add=True)

    def update_payment(self,amount):
        if self.user.salary>=amount:
            self.user.salary-=amount
            self.total_paid+=amount
            self.user.save()
            self.save()
            return True
        return False
    def __str__(self):
        return f"{self.user.username}- paid:{self.total_paid}"


