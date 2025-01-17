from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.conf import settings
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# id rzp_test_aSaMOLmp1IqtHq
# key haSLsc4y4NaBBaUU2SvWoKvb

def home(req):
    return render(req,"index.html")

def order_payment(req):
    if req.method == "POST":
        name = req.POST.get("name")
        amount = req.POST.get("amount")
        client = razorpay.Client(auth=(settings.RAZOPAY_KEY_ID,settings.RAZOPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency" : "INR", "payment_capture" : "1"}
        )
        order_id = razorpay_order['id']
        order =Order.objects.create(
            name=name,amount=amount,provider_order_id=order_id
        )
        order.save()
        return render(
            req,"index.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "razorpay/callback",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
            },  
        )
    return render(req,"index.html")

@csrf_exempt

