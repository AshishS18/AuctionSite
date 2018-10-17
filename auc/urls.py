
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from auction import views
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('addauction/', views.add_auction, name='addauction'),
    path('productadded/', views.add_auction, name='productadded'),
    path('auction/<int:id>/', views.view_auction),
    path('bidauction/<int:id>/', views.bid_auction, name='bidauction'),
    path('admin/', admin.site.urls),
    path('userlist/', views.UserList.as_view(), name='user_list'),
    path('auctionlist/', views.AuctionList.as_view(), name='auction_list'),
    path('auctionlist/<int:id>', views.AuctionDetail.as_view(), name='auction_lists'),
    path('bidlist/', views.BidList.as_view(), name='bid_list'),
    path('auctions', views.auctionPage, name='auction'),
    path('auctions/<int:id>', views.auctionPage, name='auction'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)