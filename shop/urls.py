from django.urls import path,include
from . import views
urlpatterns = [

    path('home/',views.home, name= 'home'),
    
    path('register/',views.register, name = 'register'),
    path('login/',views.loginpage, name = 'loginpage'),
    
    path('collection/',views.collection, name = 'collection'),
    path('collection_view/<str:name>',views.collection_view, name = 'collection_view'),
    path('product_detail/<str:pname>',views.product_detail, name = 'product_detail'),
    
    
    
]
