from django.contrib import admin
from .models import User,Event,Attendance,Payment
from django.utils.html import format_html
from payment.views import stk_push  # Import STK push function

from django.contrib import admin
from django.utils.html import format_html
from .models import User, Event, Attendance, Payment
from payment.views import stk_push  # Import STK push function from payment app

    
# Register your models here.
admin.site.register(User)
admin.site.register(Event)
#admin.site.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'date', 'overtime_hours', 'calculate_pay_display', 'send_payment')

    def calculate_pay_display(self, obj):  # Accepts obj as an argument
        return obj.calculate_pay()  # Call the method on the object

    calculate_pay_display.short_description = "Pay"  # Rename column in admin panel

    def send_payment(self, obj):
        url = f"/payment/stk_push/{obj.pk}/"  # Ensure this matches your urlpatterns
        return format_html('<a href="{}" class="button" style="background: #28a745; color: white; padding: 5px 10px; text-decoration: none; border-radius: 5px;">Send STK Push</a>', url)

    send_payment.short_description = "STK Push Payment"

# Register the model
admin.site.register(Attendance, AttendanceAdmin)



