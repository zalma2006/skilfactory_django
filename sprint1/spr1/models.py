from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class Users(models.Model):
    email = models.EmailField(unique=True)
    fam = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    otc = models.CharField(max_length=150)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$',
                                 message="Phone number must be entered in the format: "
                                         "'+999999999'. Up to 12 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=14, blank=True)


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.FloatField()


class Image(models.Model):
    title = models.CharField(max_length=255)
    data = models.ImageField(max_length=4000, upload_to='uploads/')


class PerevalAdded(models.Model):
    new, pending, accepted, rejected = 'new', 'pending', 'accepted', 'rejected'
    changes = [(new, 'new'), (pending, 'pending'), (accepted, 'accepted'),
               (rejected, 'rejected')]
    beauty_title = models.CharField(max_length=255)
    title = models.CharField(null=False, max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.CharField(max_length=1)
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE)
    winter = models.CharField(max_length=100)
    summer = models.CharField(max_length=100)
    autumn = models.CharField(max_length=100)
    spring = models.CharField(max_length=100)
    images = models.ForeignKey(Image, on_delete=models.CASCADE)
    status = models.CharField(choices=changes, max_length=8)
