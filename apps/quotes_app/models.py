# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.
from ..lr_app.models import Users
class QuotesManager(models.Manager):
    """
    Manager Class for Class Quotes

    Attributes:
        getUnfavoritedQuotes (u_id): gets all quotes that are not favorited by the user

        add_quote(data, u_id): adds a quote to the database
    """
    def getUnfavoritedQuotes(self, u_id):
        """
        Gets users unfavorited quotes

        Args:
            u_id (int): unique id of a user
        
        Returns:
            list: a list of responses from the manager, the response list is filled by Quote objects
        """
        response = []
        all_quotes = Quotes.objects.all().order_by('-id')
        for quote in all_quotes:
            if len(quote.favorited_by.filter(id=u_id)) == 0:
                response.append(quote)
        return response

    def add_quote(self, data, u_id):
        """
        Adds a quote to the database

        Args:
            data (request.POST): post data from a form
            
            u_id (int): unique id of the user who posted the form
        
        Returns:
            list: a list of responses from the manager, if any response is given, the request is rejected
        """
        response = []
        if len(data['quoted_by']) < 4:
            response.append('Name must be more than three characters long!')

        if len(data['quote']) < 11:
            response.append('Quote must be more than 10 characters long!')
        
        if len(response) == 0:
            Quotes.objects.create(
                quoted_by = data['quoted_by'],
                quote = data['quote'],
                posted_by = Users.objects.get(id=u_id)
            )
        return response

    def add_to_user_fav(self, u_id, q_id):
        """
        Adds a quote to a users favorites list

        Args:
            u_id (int): unique id of the user who favoritied the quote

            q_id (int): unique id of the quote that was favorited
        
        Returns:
            class context: self
        """
        this_user = Users.objects.get(id=u_id)
        this_quote= Quotes.objects.get(id=q_id)
        this_user.favorite_quotes.add(this_quote)
        return self

    def remove_from_user_fav(self, u_id, q_id):
        """
        Removes a quote from a users favorites list

        Args:
            u_id (int): unique id of the user who wants the quote removed from their list

            q_id (int): unique id of the quote that was requested to be remove from their list

        Returns:
            class context: self
        """
        this_user = Users.objects.get(id=u_id)
        this_quote= this_user.favorite_quotes.all().get(id=q_id)
        this_user.favorite_quotes.remove(this_quote)
        return self

class Quotes(models.Model):
    """
    Quotes class: contains all fields of the table quotes_app_quotes
    """
    quoted_by = models.CharField(max_length=255)
    quote = models.TextField()
    favorited_by = models.ManyToManyField(Users, related_name="favorite_quotes")
    posted_by = models.ForeignKey(Users, related_name="poster_of")
    objects = QuotesManager()