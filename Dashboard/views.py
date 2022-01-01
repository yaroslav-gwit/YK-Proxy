from django.shortcuts import render, redirect
from django.db.models import F
from pathlib import Path
import os
from HAProxyManager import settings
from Users import models as user_models
from Certificates import models as certificate_models
from Sites import models as site_models

from datetime import datetime, timedelta

# Create your views here

def dashboard(request):
    page_name = "Dashboard"

    users = user_models.User.objects.all
    users_top_5 = user_models.User.objects.order_by(F('date_created').desc())[:5]
    users_disabled = user_models.User.objects.all().filter(disabled="Yes")
    users_locked_out = user_models.User.objects.all().filter(locked_out="Yes")
    users_active = users

    sites = site_models.Site.objects.order_by(F('date_created').desc())[:5]
    sites_for_charts = site_models.Site.objects.all()
    sites_for_charts_disabled = site_models.Site.objects.all().filter(disabled="Yes")
    sites_for_charts_under_maintenance = site_models.Site.objects.all().filter(under_maintenance="Yes")
    sites_for_charts_backends_active = site_models.BackendServer.objects.all()
    sites_for_charts_backends_failed = site_models.BackendServer.objects.all().filter(probe_status="failed")
    sites_for_charts_backends_disabled = site_models.BackendServer.objects.all().filter(backend_enabled="No")

    certificates = certificate_models.Certificate.objects.order_by(F('date_created').desc())[:5]
    certificates_for_charts = certificate_models.Certificate.objects.all()
    certificates_for_charts_disabled = certificate_models.Certificate.objects.all().filter(disabled="Yes")
    date_now = datetime.now()
    certificates_for_charts_expired = certificate_models.Certificate.objects.filter(expiration_date__lt=date_now)
    
    # COLORS FOR GRAPHS
    green_inner_color = "rgba(49, 255, 0, 0.2)"
    green_outer_color = "rgba(49, 255, 0, 1)"
    blue_inner_color = "rgba(54, 162, 235, 0.2)"
    blue_outer_color = "rgba(54, 162, 235, 1)"
    yellow_inner_color = "rgba(255, 206, 86, 0.2)"
    yellow_outer_color = "rgba(255, 206, 86, 1)"
    red_inner_color = "rgba(255, 99, 132, 0.2)"
    red_outer_color = "rgba(255, 99, 132, 1)"
    violet_inner_color = "rgba(141, 153, 174, 0.2)"
    violet_outer_color = "rgba(141, 153, 174, 1)"
    # EOF COLORS FOR GRAPHS
    
    context = {
        'page_name': page_name,

        'date_now':date_now,
        
        'users': users,
        'users_top_5':users_top_5,
        'users_disabled':users_disabled,
        'users_active':users_active,
        'users_locked_out':users_locked_out,
        
        'green_inner_color':green_inner_color,
        'green_outer_color':green_outer_color,
        'blue_inner_color':blue_inner_color,
        'blue_outer_color':blue_outer_color,
        'yellow_inner_color':yellow_inner_color,
        'yellow_outer_color':yellow_outer_color,
        'red_inner_color':red_inner_color,
        'red_outer_color':red_outer_color,
        'violet_inner_color':violet_inner_color,
        'violet_outer_color':violet_outer_color,
        
        'certificates': certificates,
        'certificates_for_charts':certificates_for_charts,
        'certificates_for_charts_disabled':certificates_for_charts_disabled,
        'certificates_for_charts_expired':certificates_for_charts_expired,
        
        'sites': sites,
        'sites_for_charts':sites_for_charts,
        'sites_for_charts_disabled':sites_for_charts_disabled,
        'sites_for_charts_under_maintenance':sites_for_charts_under_maintenance,
        'sites_for_charts_backends_active':sites_for_charts_backends_active,
        'sites_for_charts_backends_failed':sites_for_charts_backends_failed,
        'sites_for_charts_backends_disabled':sites_for_charts_backends_disabled
    }
    return render(request, "Dashboard/main.html", context)
