from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    return redirect('dashboard')
