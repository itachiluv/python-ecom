from django.urls import path,include
from . import views
urlpatterns = [

    path('home/',views.home, name= 'home'),
    
    path('register/',views.register, name = 'register'),
    
    path('login/',views.loginpage, name = 'loginpage'),
    path('logout/',views.logoutpage, name = 'logoutpage'),
    
    path('addcart/',views.addcart,name = 'addcart'),
    path('cart/',views.cart_page, name = 'cart'),
    path('remove_cart/<str:id>',views.remove_cart, name = 'remove_cart'),
    path('fav/',views.fav_page, name = 'fav'),
    path('fav_view_page/',views.fav_view_page, name = 'fav_view_page'),
    path('remove_fav/<str:id>',views.remove_fav, name = 'remove_fav'),
    
    path('collection/',views.collection, name = 'collection'),
    path('collection_view/<str:name>',views.collection_view, name = 'collection_view'),
    path('product_detail/<str:pname>',views.product_detail, name = 'product_detail'),
    
    
    
]
