import hashlib

#http://ccbv.co.uk
from django.views.generic import ListView, DetailView
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from shoping.apps.epayco.models import EpayCo
from .models import Item


class ItemListView(ListView):
    model = Item

class ItemDetailView(DetailView):
    model = Item
