from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json
from django.http import JsonResponse
# Create your views here.
def home(request):
    products = Product.objects.filter(trending = 1)
    context = {
        'products':products
    }
    return render(request,'shop/index.html',context)

def remove_cart(request,id):
    cart_del = cart.objects.get(id = id)
    cart_del.delete()
    return redirect('cart')

def remove_fav(request,id):
    cart_del = Fav.objects.get(id = id)
    cart_del.delete()
    return redirect('fav_view_page')

def fav_view_page(request):
    if request.user.is_authenticated:
        fav = Fav.objects.filter(user = request.user)
        context = {
            'fav':fav
        }
        return render(request,'shop/fav.html',context)
    else:
        return redirect('home')

def fav_page(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            product_id = data.get('pid')
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Fav.objects.filter(user = request.user.id, product_id= product_id):
                    return JsonResponse({'status': 'Product Already in Favourite'}, status=200)       
                else: 
                    Fav.objects.create(
                        user = request.user,
                        product_id = product_id
                    )
                    return JsonResponse({'status': 'Product Add to Favourite'}, status=200)
        else:
            return JsonResponse({'status': 'Login to Add Favourites'}, status=200)
    else:
        
        return JsonResponse({'status': 'Invalid request'}, status=200)
    

# def addcart(request):
#     pass
    # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    #     if request.user.is_authenticated:
    #         data = json.load(request)
    #         product_qty = data['product_qty']
    #         product_id = data['pid']
    #         print('User --->',request.user)
    #         print("Cart Details ---->",cart.objects.filter(user=request.user.id,product_id = product_id))
    #         product_status = Product.objects.get(id=product_id)
    #         print('Product Status--->',product_status)
    #         if product_status:
    #             if cart.objects.filter(user=request.user.id,product= product_id):
    #                 return JsonResponse({'status':'Product Already in Cart'},status =200)
    #             else:
    #                 if product_status.qty>=product_qty:
    #                     cart.objects.create(
    #                         user = request.user,
    #                         product = product_id,
    #                         product_qty = product_qty
    #                     )
    #                     return JsonResponse({'status':'Product Add To Cart'},status =200)
    #     else:
    #         return JsonResponse({'status':'Login to Add Cart'},status =200)
    # else:
    #     return JsonResponse({'status':'invalid access'},status =200)
    
    
def addcart(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                # Parse JSON data from the request body
                data = json.loads(request.body)
                product_qty = data.get('product_qty')
                product_id = data.get('pid')

                # Retrieve the Product instance using the product_id
                try:
                    product_instance = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    return JsonResponse({'status': 'Product does not exist'}, status=404)

                # Check if the product is already in the cart for the current user
                if cart.objects.filter(user=request.user, product=product_instance).exists():
                    return JsonResponse({'status': 'Product already in cart'}, status=200)
                else:
                    # Check if the desired quantity is available
                    if product_instance.qty >= product_qty:
                        # Create a new cart entry
                        cart.objects.create(
                            user=request.user,
                            product=product_instance,
                            product_qty=product_qty
                        )
                        return JsonResponse({'status': 'Product added to cart'}, status=200)
                    else:
                        # Return a response if quantity is not available
                        return JsonResponse({'status': 'Not enough quantity available'}, status=400)
            except json.JSONDecodeError:
                # Handle JSON parsing error
                return JsonResponse({'status': 'Invalid JSON data'}, status=400)
        else:
            return JsonResponse({'status': 'Please log in to add to cart'}, status=403)
    else:
        # Handle invalid request method (not an AJAX request)
        return JsonResponse({'status': 'Invalid request method'}, status=400)
    
    
def cart_page(request):
    if request.user.is_authenticated:
        cart_detail = cart.objects.filter(user = request.user)
        context = {
            'cart_detail':cart_detail
        }
        return render(request,'shop/cart.html',context)
    else:
        return redirect('home')

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request,username=username,password = password)
            if user is not None:
                login(request,user)
                messages.success(request,'Login Successfully')
                return redirect('home')
            else:
                messages.error(request,'Invalide Username and Password')
                return redirect('loginpage')
            
        return render(request,'shop/login.html')

def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'Logout Successfull')
    return redirect('home')
    

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