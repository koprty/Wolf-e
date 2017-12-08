"""WolfieShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from shop import views as shop_view

#for if we want to recreate another admin login portal
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', shop_view.index, name='index'),
    url(r'^item/(?P<item_id>[0-9]+)/$', shop_view.item_detail, name='item_detail'),
    
    url(r'^shoppingcart/$', shop_view.shoppingcart_detail, name='shoppingcart_detail'),
     url(r'^shoppingcart/checkout/$', shop_view.checkout, name='checkout'),
     url(r'^shoppingcart/delete/(?P<customer_id>[0-9]+)/(?P<item_id>[0-9]+)$', shop_view.shoppingcart_delete, name='shoppingcart_delete'),

    url(r'^transaction/(?P<transaction_id>[0-9]+)/$', shop_view.transaction_detail, name='transaction_detail'),
    #given transactionid, want to print info from transactioncontents

    # this is for admin login... we will use this to make the login page prettier later if we have time
    url(r'^login/$', shop_view.customer_login, name='customer_login'),

    url(r'^register/$', shop_view.customer_register, name='customer_register'),
    # Some generic logout page for debugging and possibly later
    # url(r'^logout/$', auth_views.login, {'template_name': 'logout.html'})
    url(r'^logout/$', shop_view.logout, name='customer_logout'),


    url(r'^payment/$', shop_view.add_payment, name='add_payment'),
    url(r'^shipping/$', shop_view.add_shipping, name='add_shipping'),
    url(r'^confirm/$', shop_view.confirm_order, name='confirm_order'),
    url(r'^done/$', shop_view.processed_order, name='processed_order')


    #obviously access to these sc pages wouldn't actually be given to the customer. The customer would get a page
    #after logging in however that is exclusively his/her shopping cart. To be changed after customer login implemented
]
