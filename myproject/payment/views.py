from django.shortcuts import render
from django.conf import settings
import requests
import json
import base64
from django.http import JsonResponse
from datetime import datetime
from .utils import get_access_token
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
from myapp.models import User


# Create your views here.

@csrf_exempt
def stk_push(request):
    """payment=Payment.objects.all().get()
    phone_number=payment.user.phone_number

    if not phone_number.startswith('254'):
        phone_number=f"254{phone_number[-9:]}"""
    
    access_token=get_access_token()
    if not access_token:
        return JsonResponse({'error':'Failed to get access token'})
    else:
        url=f"{settings.MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest"
        timestamp=datetime.now().strftime("%Y%m%d%H%M%S")
        password=f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}".encode()
        password=base64.b64encode(password).decode()
    

        payload={
            "BusinessShortCode": settings.MPESA_SHORTCODE,  # Your business paybill/till number
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerBuyGoodsOnline",  # Change based on use case
            "Amount": 1,  # Modify as needed
            "PartyA":'254705962256',  # The customer making payment
            "PartyB":174379,  # The till number receiving payment
            "PhoneNumber":'254705962256',  # Customer's phone number
            "CallBackURL": "http://7c21-41-90-172-219.ngrok-free.app/mpesa_callback",
            "AccountReference": "Test Payment",
            "TransactionDesc": "Payment for services"
        
        }

        headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
        response = requests.post(url, json=payload, headers=headers)
    
        return JsonResponse(response.json())
    

 




import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        try:
            print("Hello World")  # Debugging step
            raw_body = request.body.decode("utf-8")
            logger.info(f"Received M-Pesa callback: {raw_body}")
            print("Received M-Pesa callback:", raw_body)  # Debugging

            data = json.loads(raw_body)

            # ✅ Handling STK Push response
            if "Body" in data and "stkCallback" in data["Body"]:
                stk_callback = data["Body"]["stkCallback"]
                result_code = stk_callback.get("ResultCode", "")
                result_desc = stk_callback.get("ResultDesc", "")
                
                callback_metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
                payment_data = {item["Name"]: item.get("Value", "") for item in callback_metadata}

                amount = payment_data.get("Amount")
                receipt_number = payment_data.get("MpesaReceiptNumber")
                phonenumber = payment_data.get("PhoneNumber")
                transaction_date = payment_data.get("TransactionDate")

                user =User.objects.filter(phone_number=phonenumber).first()
                if not user:
                    print(f"User with phone number {phonenumber} not found")
                    return JsonResponse({'error ':'User phone number not found'})

            # ✅ Handling Lipa na M-Pesa (C2B) response
            elif "Result" in data:
                result = data["Result"]
                result_code = result.get("ResultCode", "")
                result_desc = result.get("ResultDescription", "")

                result_param = result.get("ResultParameters", {}).get("ResultParameter", [])
                payment_data = {item["Key"]: item.get("Value", "") for item in result_param}

                amount = payment_data.get("TransactionAmount")
                receipt_number = payment_data.get("TransactionReceipt")
                phone_number = payment_data.get("ReceiverPartyPublicName", "").split("-")[0]

            else:
                return JsonResponse({'error': 'Unknown M-Pesa response format'}, status=400)

            # ✅ Process successful payment
            if result_code == 0:
                if user.salary>=amount:
                    salary-=amount
                    user.save()
                    Payment.objects.create(user=user,total_paid=amount,last_payment_date=transaction_date)
                print(f"Payment successful! Amount: {amount}, Receipt: {receipt_number}, Phone: {phone_number}")
                return JsonResponse({'message': 'Payment processed successfully'})
                

            else:
                print(f" Payment failed: {result_desc}")
                return JsonResponse({'error': f"Payment failed: {result_desc}"}, status=400)

        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        except Exception as e:
            logger.error(f"Error processing M-Pesa callback: {str(e)}")
            return JsonResponse({'error': f'Something went wrong: {str(e)}'}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)
