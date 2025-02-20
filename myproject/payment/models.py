from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model

# Create your models here.
class Payment(models.Model):
    user=models.ForeignKey('myapp.User',on_delete=models.CASCADE)
    total_paid=models.DecimalField(max_digits=10,decimal_places=2 ,default=0.00)
    last_payment_date=models.DateField(auto_now_add=True)
    Total_billed=models.DecimalField(max_digits=10, decimal_places=2,default=0.00)

    def make_payment(self,amount):
        if self.user.salary>=amount:
            self.user.salary-=amount
            self.total_paid+=amount
            self.user.save()
            self.save()
            return True  
        return False
    def __str__(self):
        return f"{self.user.name}-{self.total_paid}"