from django.shortcuts import render
from .models import *
# Create your views here.
def home(request):
    
    return render(request,'shop/index.html')

def register(request):
    
    return render(request,'shop/register.html')

def collection(request):
    catagory = Catagory.objects.all()
    context = {
        'catagory':catagory
    }
    
    return render(request,'shop/collection.html',context)