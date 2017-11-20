# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from ..lr_app.models import Users
from models import Quotes

from django.contrib.messages import warning
# Create your views here.
def display_quotes(request):
    """
    Route for rendering the main quotes page
    """
    if 'id' not in request.session:
        return redirect('/main')
    context = {
        "user": Users.objects.get(id=request.session['id']),
        "favorites": Users.objects.get(id=request.session['id']).favorite_quotes.all().order_by('-id'),
        "quotes": Quotes.objects.getUnfavoritedQuotes(request.session['id'])
    }
    return render(request, 'quotes/quotes.html', context)

def add_quote(request):
    """
    Route for processing a quote to be added to the database
    """
    if request.method == 'POST':
        response = Quotes.objects.add_quote(request.POST, request.session['id'])
        if len(response) != 0:
            for message in response:
                warning(request, message)
    return redirect('/quotes')

def add_to_fav(request, q_id):
    """
    Route for processing a quote to be added as a favorite to a user

    Args:
        q_id (int): unique id of the quote that will be added to the requested user
    """
    if request.method == 'POST':
        Quotes.objects.add_to_user_fav(request.session['id'], q_id)
    return redirect('/quotes')

def remove_from_fav(request, q_id):
    """
    Route for processing a quote to be removed as a favorite of a user
    
    Args:
        q_id (int): unique id of the quote that will be removed from the requested user
    """
    if request.method == 'POST':
        Quotes.objects.remove_from_user_fav(request.session['id'], q_id)
    return redirect('/quotes')