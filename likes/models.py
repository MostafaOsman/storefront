from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Liked_Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE) #identify the type of object that the user likes
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey() # for reading an actual object
