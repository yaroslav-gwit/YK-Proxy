from django.db import models
from django.urls import reverse
import datetime

# Create your models here.

class BackendServer(models.Model):

    YES_OR_NO = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    HTTP_VERSION = (
        ('HTTP', 'HTTP'),
        ('HTTP/2', 'HTTP/2'),
    )

    HTTP_ENCRYPTION = (
        ('HTTP', 'HTTP'),
        ('HTTPs', 'HTTPs'),
    )

    PROBE_STATUS = (
        ('active', 'active'),
        ('failed', 'failed'),
    )

    backend_server_name = models.CharField(max_length=100, unique=True, null=True)
    backend_address = models.CharField(max_length=100)
    backend_enabled = models.CharField(max_length=5, choices=YES_OR_NO, default='Yes')
    http_version = models.CharField(max_length=10, choices=HTTP_VERSION, default='HTTP')
    http_encryption = models.CharField(max_length=10, choices=HTTP_ENCRYPTION, default='HTTP')
    probe_status = models.CharField(max_length=10, choices=PROBE_STATUS, default='active')
    ignore_self_signed_ssl = models.CharField(max_length=5, choices=YES_OR_NO, default='Yes')

    def __str__(self):
        return '%s %s' % (self.backend_server_name, self.backend_address) 


class Site(models.Model):

    HTTP_VERSION = (
        ('HTTP', 'HTTP'),
        ('HTTP/2', 'HTTP/2'),
    )

    HTTP_ENCRYPTION = (
        ('HTTP', 'HTTP'),
        ('HTTPs', 'HTTPs'),
    )
    
    YES_OR_NO = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    site_id = models.IntegerField(unique=True, null=True)
    site_address = models.CharField(max_length=100, default='Blank', unique=True)
    certificate_address = models.ForeignKey('Certificates.Certificate', null=True, default=None, on_delete=models.CASCADE, related_name='site_certificate_address')
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(default=datetime.datetime.now())
    #site_certificate_expiry_date = models.ForeignKey('Certificates.Certificate', null=True, default=None, on_delete=models.CASCADE, related_name='site_certificate_expiry_date')
    created_by = models.ForeignKey('Users.User', null=True, default=None, on_delete=models.CASCADE, blank=True, related_name='site_created_by')
    admin_users = models.ManyToManyField('Users.User', default=None, blank=True, related_name='site_admin_users')
    read_write_users = models.ManyToManyField('Users.User', default=None, blank=True, related_name='site_read_write_users')
    read_only_users = models.ManyToManyField('Users.User', default=None, blank=True, related_name='site_read_only_users')
    disabled = models.CharField(max_length=5, choices=YES_OR_NO, default='No')
    under_maintenance = models.CharField(max_length=5, choices=YES_OR_NO, default='No')
    backend_servers = models.ManyToManyField(BackendServer, default=None, blank=True, related_name='site_backend_servers')
    #http_version = models.CharField(max_length=10, choices=HTTP_VERSION, default='HTTP')
    #http_encryption = models.CharField(max_length=10, choices=HTTP_ENCRYPTION, default='HTTP')
    www_redirect = models.CharField(max_length=5, choices=YES_OR_NO, default='Yes')

    def __str__(self):
        return self.site_address