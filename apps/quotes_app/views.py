# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from ..lr_app.models import Users
from models import Quotes

from django.contrib.messages import warning
# Create your views here.
def display_quotes(request):
    if 'id' not in request.session:
        return redirect('/main')
    context = {
        "user": Users.objects.get(id=request.session['id']),
        "favorites": Users.objects.get(id=request.session['id']).favorite_quotes,
        "quotes": Quotes.objects.getUnfavoritedQuotes(request.session['id'])
    }
    return render(request, 'quotes/quotes.html', context)

def add_quote(request):
    if request.method == 'POST':
        response = Quotes.objects.add_quote(request.POST, Users.objects.get(id=request.session['id']))
        if len(response) != 0:
            for message in response:
                warning(request, message)
    return redirect('/quotes')