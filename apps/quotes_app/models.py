# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.
from ..lr_app.models import Users
class QuotesManager(models.Manager):
    def getUnfavoritedQuotes(self, u_id):
        response = []
        all_quotes = Quotes.objects.all()
        for quote in all_quotes:
            if len(quote.favorited_by.filter(id=u_id)) == 0:
                response.append(quote)
        return response

    def add_quote(self, data, u_id):
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

class Quotes(models.Model):
    quoted_by = models.CharField(max_length=255)
    quote = models.TextField()
    favorited_by = models.ManyToManyField(Users, related_name="favorite_quotes")
    posted_by = models.ForeignKey(Users, related_name="poster_of")
    objects = QuotesManager()