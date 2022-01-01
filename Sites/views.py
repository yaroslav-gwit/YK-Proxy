from django.shortcuts import render, redirect
from django.db.models import F
from pathlib import Path
import os
from HAProxyManager import settings
from Sites import models as site_models
from Users import models as user_models
from Certificates import models as certificate_models
import subprocess
from django.http import HttpResponseRedirect

from datetime import datetime
import re

# Create your views here

def sites(request):
    sites = site_models.Site.objects.order_by(F('site_address').asc())

    date_now = datetime.now()

    page_name = "Sites"
    context = { 
        'page_name':page_name,
        'date_now':date_now,
        'sites':sites,
        }
    return render(request, "Sites/main.html", context)

def delete_site(request, site_id, ):
    select_site_id = site_models.Site.objects.get(site_id=site_id)
    select_site_id.delete()
    # return redirect('sites')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def disable_site(request, site_id, disabled_status):
    select_site_id = site_models.Site.objects.get(site_id=site_id)
    if disabled_status == "No":
        disable = "Yes"
    else:
        disable = "No"
    select_site_id.disabled = disable
    select_site_id.save(update_fields=['disabled'])
    # return redirect('sites')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def maintenance_site(request, site_id, maintenance_status):
    select_site_id = site_models.Site.objects.get(site_id=site_id)
    if maintenance_status == "No":
        maintenance = "Yes"
    else:
        maintenance = "No"
    select_site_id.under_maintenance = maintenance
    select_site_id.save(update_fields=['under_maintenance'])
    # return redirect('sites')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def create_new_site(request):
    users = user_models.User.objects.all()
    date_now = datetime.now()

    success_message = ""

    if request.method == 'POST':
        frontend_adress = request.POST.get('FrontEndAddress')
        
        if request.POST.get('WwwRedir') == "on":
            www_redirect = "Yes"
        else:
            www_redirect = "No"
        
        # if request.POST.get('HTTPs') == "on":
        #     http_encryption = "HTTPs"
        # else:
        #     http_encryption = "HTTP"
        
        # if request.POST.get('HTTP2') == "on":
        #     http_version = "HTTP/2"
        # else:
        #     http_version = "HTTP"

        if request.POST.get('Certificate') == "on":
            certificate_domain = request.POST.get('FrontEndAddress')
        else:
            certificate_domain = request.POST.get('FrontEndAddress') + ".selfsigned"

        # Backend servers portion which determines if there should be one or many servers and saves them to DB
        if request.POST.get('BackendHTTPs') == "on":
            backend_http_encryption = "HTTPs"
        else:
            backend_http_encryption = "HTTP"

        if request.POST.get('BackendHTTP2') == "on":
            backend_http_version = "HTTP/2"
        else:
            backend_http_version = "HTTP"

        if request.POST.get('BackendCertificate') == "on":
            backend_ignore_self_signed = "Yes"
        else:
            backend_ignore_self_signed = "No"
        
        backend_servers = request.POST.get('BackendServers')
        
        backend_servers_applied = []

        if re.match(".*, ", backend_servers):
            backend_servers_list_beg = backend_servers.split(", ")
            backend_servers_list_finish = []

            for i in range(0, len(backend_servers_list_beg)):
                backend_servers_list_finish.append(backend_servers_list_beg[i].split(" "))

            for i in range(0, len(backend_servers_list_finish)):
                create_be = site_models.BackendServer.objects.create(backend_server_name=backend_servers_list_finish[i][0], backend_address=backend_servers_list_finish[i][1], http_version=backend_http_version, http_encryption=backend_http_encryption, ignore_self_signed_ssl=backend_ignore_self_signed, )
                backend_servers_applied.append(backend_servers_list_finish[i][0])

        else:
            backend_servers_list = backend_servers.split(" ")
            create_be = site_models.BackendServer.objects.create(backend_server_name=backend_servers_list[0], backend_address=backend_servers_list[1], http_version=backend_http_version, http_encryption=backend_http_encryption, ignore_self_signed_ssl=backend_ignore_self_signed, )
            backend_servers_applied.append(backend_servers_list[0])
        # EOF Backend servers portion which determines if there should be one or many servers and saves them to DB

        created_by = request.POST.get('CreatedBy')
        managed_by = []
        managed_by.append(request.POST.get('ManagedBy'))
        manager_role = request.POST.get('ManagerRole')

        save_certificate = certificate_models.Certificate.objects.create(domain_name=frontend_adress, created_by=user_models.User.objects.get(username = created_by))
        
        save_site = site_models.Site.objects.create(site_address=frontend_adress, www_redirect=www_redirect, certificate_address=certificate_models.Certificate.objects.get(domain_name = frontend_adress))
        save_site.created_by = user_models.User.objects.get(username = created_by)

        backend_servers_objects_filter = site_models.BackendServer.objects.filter(backend_server_name__in = backend_servers_applied)
        # Or use save_site.backend_servers.add(*backend_servers_objects_filter) to add more items to the existing record, instead of setting the list
        backend_servers_save = save_site.backend_servers.set(backend_servers_objects_filter)
        
        users_managed_by = user_models.User.objects.filter(username__in = managed_by)

        if manager_role == "AdminUser":
            save_site.admin_users.set(users_managed_by)
            save_certificate.admin_users.set(users_managed_by)
        if manager_role == "ReadWriteUser":
            save_site.read_write_users.set(users_managed_by)
            save_certificate.read_write_users.set(users_managed_by)
        if manager_role == "ReadOnlyUser":
            save_site.read_only_users.set(users_managed_by)
            save_certificate.read_only_users.set(users_managed_by)
        
        save_certificate.save()
        save_site.save()

        # Certbox get the cert, HAProxy generate the config and reload the service
        command = 'bash -c "if [[ ! -d /ssl/ ]]; then mkdir /ssl/; fi"'
        subprocess.run(command, shell=True, stdout=None)

        if len(os.listdir('/ssl') ) == 0:
            command = "curl localhost:8002/sites/haproxy-generate-template/ > /etc/haproxy/haproxy.cfg"
            subprocess.run(command, shell=True, stdout=None)

            command = "systemctl reload haproxy"
            subprocess.run(command, shell=True, stdout=None)
        
        command = "certbot certonly --standalone -d " + frontend_adress + " --non-interactive --agree-tos --email=slv@yari.pw --http-01-port=8888"
        subprocess.run(command, shell=True, stdout=None)

        command = "cat /etc/letsencrypt/live/" + frontend_adress + "/fullchain.pem /etc/letsencrypt/live/" + frontend_adress + "/privkey.pem > /ssl/" + frontend_adress + ".pem"
        subprocess.run(command, shell=True, stdout=None)

        if www_redirect == "Yes":
            command = "certbot certonly --standalone -d www." + frontend_adress + " --non-interactive --agree-tos --email=slv@yari.pw --http-01-port=8888"
            subprocess.run(command, shell=True, stdout=None)

            command = "cat /etc/letsencrypt/live/www." + frontend_adress + "/fullchain.pem /etc/letsencrypt/live/www." + frontend_adress + "/privkey.pem > /ssl/www." + frontend_adress + ".pem"
            subprocess.run(command, shell=True, stdout=None)

        command = "curl localhost:8002/sites/haproxy-generate-template/ > /etc/haproxy/haproxy.cfg"
        subprocess.run(command, shell=True, stdout=None)

        command = "systemctl reload haproxy"
        subprocess.run(command, shell=True, stdout=None)
        # EOF Certbox get the cert, HAProxy generate the config and reload the service

        success_message = "Site " + frontend_adress + " was created!"

    page_name = "Create new site"
    context = {
        'page_name': page_name,
        'success_message': success_message,
        'date_now':date_now,
        'users':users,
    }

    return render(request, "Sites/create_new_site.html", context)


def haproxy_generate_template(request):
    sites = site_models.Site.objects.order_by(F('site_address').asc())
    # sites = site_models.Site.objects.all()

    if len(os.listdir('/ssl')) == 0:
        ssl_folder_empty = True
    else:
        ssl_folder_empty = False
    
    date_now = datetime.now()

    page_name = "HAProxy Template"
    context = { 
        'page_name':page_name,
        'date_now':date_now,
        'sites':sites,
        'ssl_folder_empty':ssl_folder_empty,
        }
    return render(request, "Sites/haproxy_template.html", context)