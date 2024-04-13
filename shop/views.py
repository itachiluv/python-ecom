from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib import messages
# Create your views here.
def home(request):
    products = Product.objects.filter(trending = 1)
    context = {
        'products':products
    }
    return render(request,'shop/index.html',context)

def loginpage(request):
    
    return render(request,'shop/login.html')

def register(request):
    form = CustomerUserForm()
    if request.method == 'POST':
        form = CustomerUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registraion Successfull')
            return redirect('loginpage')
    context = {
        'form':form
    }
    return render(request,'shop/register.html',context)

def collection(request):
    catagory = Catagory.objects.all()
    context = {
        'catagory':catagory
    }
    
    return render(request,'shop/collection.html',context)

def collection_view(request, name):
    if (Catagory.objects.filter(name = name)):
        
        products = Product.objects.filter(catagory__name = name)
        context = {
            'products':products,
            'name':name
        }
        return render(request,'shop/products.html',context)
    else:
        messages.warning(request,'Products Not Available, Try Again Later')
        return redirect('collection')
    
def product_detail(request,pname):
    
    if (Product.objects.filter(name = pname)):
        product = Product.objects.filter(name = pname).first()
    else:
        messages.warning(request,'No Products are availabl, Please try Again Later')
    context = {
        'product':product
    }
    return render(request,'shop/product_details.html',context)