from django.shortcuts import render, redirect
from django.db.models import F
from pathlib import Path
import os
from HAProxyManager import settings
from Certificates import models as certificate_models
from datetime import datetime

# Create your views here

def certificates(request):
    
    page_name = "Certificates"

    date_now = datetime.now()
    certificates = certificate_models.Certificate.objects.order_by(F('domain_name').asc())

    context = {
        'page_name': page_name,
        'certificates': certificates,
        'date_now':date_now
    }
    return render(request, "Certificates/main.html", context)