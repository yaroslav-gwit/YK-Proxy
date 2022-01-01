from django.db import models
from django.urls import reverse

# Create your models here.
class User(models.Model):

    ROLES = (
        ('Superadmin', 'Superadmin'),
        ('Admin', 'Admin'),
        ('User', 'User'),
    )

    YES_OR_NO = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    full_name = models.CharField(max_length=100, null=False)
    username = models.CharField(max_length=15, null=False)
    user_id = models.IntegerField(unique=True, null=False)
    email = models.CharField(max_length=200, null=True)
    role = models.CharField(max_length=50, null=False, choices=ROLES, default="User")
    locked_out = models.CharField(max_length=15, null=True, choices=YES_OR_NO, default="No")
    disabled = models.CharField(max_length=15, null=True, choices=YES_OR_NO, default="No")
    date_created = models.DateTimeField(auto_now_add=True)
    user_avatar = models.ImageField(null=True)

    def __str__(self):
        return '%s (%s)' % (self.full_name, self.username)

    # def get_absolute_url(self):
    #     """Returns the url to access a particular instance of the model."""
    #     return reverse('User', args=[str(self.username)])

    class Meta:
        ordering = ['full_name']