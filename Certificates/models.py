from django.db import models
from django.urls import reverse
# from Users.models import User
import datetime

# Create your models here.
class Certificate(models.Model):

    YES_OR_NO = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    domain_name = models.CharField(max_length=50, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(default=datetime.datetime.now())
    date_edited = models.DateTimeField(default=datetime.datetime.now())
    last_time_renewed = models.DateTimeField(default=datetime.datetime.now())
    next_renewal = models.DateTimeField(default=datetime.datetime.now())
    created_by = models.ForeignKey('Users.User', default=None, on_delete=models.CASCADE, blank=True, related_name='created_by')
    admin_users = models.ManyToManyField('Users.User', default=None, blank=True, related_name='admin_users')
    read_write_users = models.ManyToManyField('Users.User', default=None, blank=True, related_name='read_write_users')
    read_only_users = models.ManyToManyField('Users.User', default=None, blank=True, related_name='read_only_users')
    orphaned = models.CharField(max_length=5, choices=YES_OR_NO, default='No')
    disabled = models.CharField(max_length=5, choices=YES_OR_NO, default='No')

    def __str__(self):
        return self.domain_name



    # def get_absolute_url(self):
    #     """Returns the url to access a particular instance of the model."""
    #     return reverse('User', args=[str(self.domain_name)])
