"""auc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from auction import views
from django.views.decorators.csrf import csrf_exempt

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^addauction/$', views.add_auction, name='addauction'),
    url(r'^saveauction/$', views.save_auction, name='saveauction'),
    url(r'^productadded/$', views.add_auction, name='productadded'),
    path('admin/', admin.site.urls),
    path('userlist/', views.UserList.as_view(), name='user_list'),
    path('auctionlist/', views.AuctionList.as_view(), name='auction_list'),
    path('bidlist/', views.BidList.as_view(), name='bid_list'),

]