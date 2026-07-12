from django.shortcuts import render
from .models import *

def home(request):
    return render(request, 'index.html')

def index(request):
    return render(request, 'index.html')

def allocations(request):
    return render(request, 'allocations.html')

def assets(request):
    return render(request, 'assets.html')

def bookings(request):
    return render(request, 'bookings.html')

def transfers(request):
    return render(request, 'transfers.html')
