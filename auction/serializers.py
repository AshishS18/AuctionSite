from rest_framework import serializers
from auction.models import auction, bid
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = auction
        fields = ['seller_id',
                  'location',
                  'description',
                  'creation_time',
                  'start_time',
                  'end_time',
                  'base_price',
                  'title']


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = bid
        fields = ['auctioneer',
                  'user',
                  'amount',
                  'is_winning']
