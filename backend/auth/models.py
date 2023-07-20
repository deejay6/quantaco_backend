import hashlib
import os
from datetime import timedelta

from django.db import models
from django.utils import timezone


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user"

    @property
    def name(self):
        if self.first_name:
            name = str(self.first_name).strip()
        else:
            name = ""
        if self.last_name is not None:
            name = name + " " + str(self.last_name).strip()
        return name.strip()


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "session"

    @staticmethod
    def generate_token(user):
        session_obj = Session.objects.filter(user=user, is_active=True).first()
        if session_obj:
            if session_obj.created_at > (timezone.now() - timedelta(hours=1)):
                return session_obj.session_id
            else:
                session_id = str(hashlib.sha1(os.urandom(128)).hexdigest())[
                    :26
                ]

            session_obj.session_id = session_id
            session_obj.save()
            return session_id
        session_id = str(hashlib.sha1(os.urandom(128)).hexdigest())[:26]
        new_session_obj = Session.objects.create(
            user=user, session_id=session_id, is_active=True
        )
        return new_session_obj.session_id
