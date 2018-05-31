# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import re
import bcrypt
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

# Create your models here.
class UserManager(models.Manager):
    def validate_registration(self, post_data):
        errors = []
        #name/username
        if len(post_data['name'])<3 or len(post_data['username'])<3:
            errors.append("Please enter Name & Username with at least 3 characters.")
        if not re.match(NAME_REGEX, post_data['name']):
            errors.append("Please enter Name with only letters")
        if len(User.objects.filter(username=post_data['username'])) > 0:
            errors.append("Username already in use")
        #pw
        if len(post_data['password'])<8:
            errors.append("Please enter a Password with at least 8 characters.")
        if post_data['confirm_password'] != post_data['password']:
            errors.append("Passwords do not match.")
        #make User and hash pw
        if not errors:
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))
            new_user = self.create(
                name = post_data['name'],
                username = post_data ['username'],
                password = hashed
            )
            return new_user
        return errors

    def validate_login(self, post_data):
        errors = []
        # check db for post_data email
        if len(self.filter(username = post_data['username'])) > 0:#email in db
            #check pw
            user = self.filter(username = post_data['username'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('Password is incorrect')
        else:
            errors.append('Email and/or password incorrect')
        if errors:
            return errors
        return user

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    objects = UserManager()
    def __str__(self):
        return self.username

class ItemManager(models.Manager):
    def validate_item(self, post_data, user_id):
        errors = []
        if len(post_data['item_name'])<1:
            errors.append("Please enter an Item/Product")
        if len(post_data['item_name'])>1 and len(post_data['item_name'])<4:
            errors.append("Please enter an Item/Product greater than 3 characters")
        if not errors:
            created_by=User.objects.get(id=user_id)
            return self.create( #variables here match with class attributes of Trip
                name = post_data['item_name'],
                created_by_name=created_by.name,
                created_by_id=created_by.id,
            )
        return errors

class Item(models.Model):
    users=models.ManyToManyField(User, related_name="items")
    name=models.CharField(max_length=255)
    created_by_name=models.CharField(max_length=255)
    created_by_id=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects=ItemManager()
    def __str__(self):
        return self.destination
