import re

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.contrib.postgres.fields import JSONField

class DUserManager(BaseUserManager):
    def _create_user(self, mobile_no, password,**extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        email = extra_fields.pop("email", None)

        mobile_no = self.normalize_mobile_no(mobile_no)
        now = timezone.now()
        user = self.model(email=email,
                          mobile_no=mobile_no, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_user(self, mobile_no, password=None, **extra_fields):
        return self._create_user(mobile_no, password, **extra_fields)


class DUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "mobile_no"
    REQUIRED_FIELDS = ["name"]

    name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    last_activity = models.DateTimeField(default=timezone.now)


    objects = DUserManager()

    def __unicode__(self):
        return 'User: %s %s' % (self.name, self.mobile_no)

class DUSerAskedQuestion(models.Model):
    image = models.ImageField(upload_to='duseraskedquestion', blank=True)
    asked_by = models.ForeignKey('duser',on_delete=models.CASCADE)


class CatalogQuestion(models.Model):
    question = models.CharField(max_length = 200)
    video_link = models.URLField(max_length = 200)
    catalog_category_type = models.CharField(max_length = 200)
    similar_question = JSONField()

class DUSerVideoSeen(models.Model):
    seen_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    catalog_question = models.ForeignKey(CatalogQuestion,on_delete=models.CASCADE)
    seen_by = models.ForeignKey('duser',on_delete=models.CASCADE)
 





