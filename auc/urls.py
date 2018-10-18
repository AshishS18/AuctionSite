from django.urls import path
from auction import views
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
    path('userlist/<int:pk>', views.UserDetail.as_view(), name='user_detail'),

    path('auctionlist/', views.AuctionList.as_view(), name='auction_list'),
    path('auctionlist/<int:pk>', views.AuctionDetail.as_view(), name='auction_detail'),

    path('bidlist/', views.BidList.as_view(), name='bid_list'),
    path('bidlist/<int:id>', views.BidDetail.as_view(), name='bid_detail'),

    # path('auctions', views.auctionPage, name='auction'),
    # path('auctions/<int:id>', views.auctionPage, name='auction'),


    path('user', views.user_page, name='userpage')

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)