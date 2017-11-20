# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from ..lr_app.models import Users
# Create your views here.
def display_user(request, u_id):
    """
    Route for rendering a unique users page

    Args:
        u_id (int): unique id of the user that the request wants rendered
    """
    if 'id' not in request.session:
        return redirect('/main')
    context = {
        "user": Users.objects.get(id=u_id),
        "count": Users.objects.get(id=u_id).poster_of.count(),
        "posts": Users.objects.get(id=u_id).poster_of.all(),
    }
    # I dont know why but django wont let me render at users/user.html. Works in quotes though.
    return render(request, 'quotes/user.html', context)