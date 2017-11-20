# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
import re, bcrypt
# Create your models here.
class UsersManager(models.Manager):
    """
    Manager Class for Class Users

    Attributes:
        addUser (data): adds singular user to the database
    """
    def addUser(self, data):
        """
        Add a user to the database

        Args:
            data (request.POST): post data from a form
        
        Returns:
            list: a list of responses from the manager, if any response is given; that data is rejected
        """
        response = []
        if not data['name']:
            response.append('Name field cannot be left empty!')
        elif not re.match(r'^[a-zA-Z ]+$', data['name']):
            response.append('Name field can only contain alpha characters!')
            

        if not data['alias']:
            response.append('Alias field cannot be left empty!')
        elif not re.match(r'^[a-zA-Z ]+$', data['alias']):
            response.append('Alias field can only contain alpha characters!')

        if not data['email']:
            response.append('Email field cannot be left empty!')
        elif not re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', data['email']):
            response.append('Email entered is invalid!')
        elif len(Users.objects.filter(email=data['email'])) != 0:
            response.append('Email already exists!')
        
        if not data['password']:
            response.append('Password field cannot be left empty!')
        elif not re.match(r'^[a-zA-Z0-9]+$', data['password']):
            response.append('Password must only contain aplha numeric characters!')
        elif data['password'] != data['confirm_password']:
            response.append('Passwords entered do not match!')

        if not data['date_of_birth']:
            response.append('Date field cannot be left empty')
        elif data['date_of_birth'] > str(datetime.date.today()):
            response.append('We cant go back in time yet!')
        if len(response) == 0:
            Users.objects.create(
                name = data['name'],
                alias = data['alias'],
                email = data['email'],
                date_of_birth = data['date_of_birth'],
                password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            )
        return response

    def login(self, data):
        """
        Checks if request is okay to give account access

        Args:
            data (request.POST): post data from a form
        
        Returns:
            list: a list of responses from the manager, if any response is given the login attempt is not valid
        """
        response = []
        if not data['email']:
            response.append('Email field cannot be left blank!')
        elif len(Users.objects.filter(email=data['email'])) == 0:
            response.append('Email is not registered!')
        elif not bcrypt.checkpw(data['password'].encode(), Users.objects.get(email=data['email']).password.encode()):
            response.append('Password is not correct!')
        if not data['password']:
            response.append('Password field cannot be left blank!')
        return response

class Users(models.Model):
    """
    Users class: contains all fields of the table lr_app_users
    """
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    objects = UsersManager()