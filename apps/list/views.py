from __future__ import unicode_literals
from django.contrib.messages import error
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "list/index.html")

def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result)== list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id']=result.id
    return redirect('/home')

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result)== list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id']=result.id
    print request.session['user_id']
    return redirect('/home')

def home(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'my_list': Item.objects.filter(users=request.session['user_id']),
        'other_items': Item.objects.exclude(users=request.session['user_id']),
    }
    return render(request, "list/home.html", context)

def logout(request):
    del request.session['user_id']
    return redirect('/')

def add_item(request):
    return render(request, "list/add.html")

def create(request):
    user=User.objects.get(id=request.session['user_id'])
    result = Item.objects.validate_item(request.POST, request.session['user_id'])
    if type(result)== list:
        for err in result:
            messages.error(request, err)
        return redirect('/add_item')
    result.save()
    user.items.add(result)
    return redirect('/home')

def show(request, item_id):
    creator = (Item.objects.get(id=item_id).created_by_id)
    creator_int = int(creator)
    context={
        'item':Item.objects.get(id=item_id),
        'others':User.objects.filter(items=item_id).exclude(id=creator_int)
    }
    return render(request, "list/show.html", context)

def add_wishlist(request, item_id):
    user=User.objects.get(id=request.session['user_id'])
    user.items.add(item_id)
    return redirect('/home')

def remove_wishlist(request, item_id):
    user=User.objects.get(id=request.session['user_id'])
    user.items.remove(item_id)
    return redirect('/home')

def delete(request, item_id):
    Item.objects.get(id=item_id).delete()
    return redirect('/home')
