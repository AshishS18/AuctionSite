from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreateForm, createAuction
from datetime import datetime
import dateutil.parser
from .serializers import AuctionSerializer, BidSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework import generics
from .models import User, auction, bid
from .services import get_users, get_auctions
from django.http.response import JsonResponse
import pytz

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def home(request):
    # background_jobs()
    # changing status and is_winning
    auctions = auction.objects.all()
    for auc in auctions:
        if auc.start_time > datetime.now(pytz.timezone('Asia/Kolkata')):
            auc.status = 'U'
        if (auc.end_time > datetime.now(pytz.timezone('Asia/Kolkata'))) and (auc.start_time < datetime.now(pytz.timezone('Asia/Kolkata'))) and auc.status != 'A':
            auc.status = 'A'
        if (auc.end_time < datetime.now(pytz.timezone('Asia/Kolkata'))) and auc.status != 'F':
            auc.status = 'F'
        auc.save()

    bids = bid.objects.all()
    for b in bids:
        for a in bids:
            if (b.auctioneer == a.auctioneer and a != b):
                if (b.is_winning == True and a.is_winning == True):
                    if (b.amount > a.amount):
                        a.is_winning = False
                        a.save()
                    else:
                        b.is_winning = False
                        b.save()
        if (b.amount < b.auctioneer.base_price):
            b.amount = b.auctioneer.base_price + 1
            b.save()
        if (b.user == b.auctioneer.seller):
            b.delete()

    posts = auction.objects.all()
    return render(request, "home.html", {'posts': posts})


def login_view(request):
    if request.user.is_authenticated:
        message = "User logged in. Log out before log in with a new user."
        posts = auction.objects.all()
        return render(request, "home.html", {'msg': message, 'posts': posts})

    else:
        if request.method == 'POST':
            username = request.POST['username']

            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    posts = auction.objects.all()
                    message = "Log in successful"
                    return render(request, "home.html", {'msg': message, 'posts': posts})
            else:
                posts = auction.objects.all()
                message = "Log in fail"
                return render(request, "home.html", {'msg': message, 'posts': posts})
        else:
            error = "Please Sign in"
            return render(request, "login.html", {'error': error})
        return render(request, "login.html")


def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            posts = auction.objects.all()
            message = "New User is created."
            return render(request, "home.html", {'msg': message, 'posts': posts})
    else:
        form = UserCreateForm(request.POST)

    return render(request, "registration.html", {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        posts = auction.objects.all()
        message = "Log out succesfull"
        return render(request, "home.html", {'msg': message, 'posts': posts})
    else:
        posts = auction.objects.all()
        message = "No user logged in"
        return render(request, "home.html", {'msg': message, 'posts': posts})


def add_auction(request):
    if request.user.is_authenticated:
        if not request.method == 'POST':
            form = createAuction()
            return render(request, 'add_auction.html', {'form': form})

        else:
            form = createAuction(request.POST, request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                end_time = cd['end_time']
                start_time = cd['start_time']
                if (end_time - datetime.now(pytz.timezone('Asia/Kolkata'))).total_seconds() < 86400:
                    message = "The minimum duration of an auction is 24hours. You have to change the end time."
                    form = createAuction()
                    return render(request, 'add_auction.html', {'msg': message, 'form': form})

                if (start_time < datetime.now(pytz.timezone('Asia/Kolkata'))):
                    message = "The auction should start after creation."
                    form = createAuction()
                    return render(request, 'add_auction.html', {'msg': message, 'form': form})

                product = form.save(commit=False)
                product.seller = request.user
                product.image = request.FILES['image']
                file_type = product.image.url.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:
                    message = "This filetype is not supported."
                    form = createAuction()
                    return render(request, 'add_auction.html', {'msg': message, 'form': form})
                product.save()
                message = "New auction has been saved"
                return render(request, 'product_added.html', {'message': message})
            else:
                form = createAuction()
                return render(request, 'add_auction.html', {'form': form, 'error': "Not valid data"})


    else:
        message = "You have to log in first"
        posts = auction.objects.all()
        return render(request, "home.html", {'msg': message, 'posts': posts})


def bid_auction(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            amount = request.POST['am']
            auctions = auction.objects.filter(id=id)
            if auctions:
                auctions = auction.objects.get(id=id)
            else:
                msg = "Auction not found"
                return render(request, "auction.html", {'msg': msg})

            if auctions.status != 'A':
                msg = "Auction not active"
                return render(request, "auction.html", {'auctioneer': auctions, 'msg': msg})
            if request.user == auctions.seller:
                msg = "Can not bid on your own auction"
                return render(request, "auction.html", {'auctioneer': auctions, 'msg': msg})
            if auctions.base_price > float(amount) or (float(amount) - auctions.base_price < 1):
                msg = "Amount have to be at least 1 greater than minimum price."
                return render(request, "auction.html", {'auctioneer': auctions, 'msg': msg})

            prev_bid_winning = bid.objects.filter(is_winning=True, auctioneer=auctions)
            if prev_bid_winning:
                prev_bid_winning = bid.objects.filter(is_winning=True, auctioneer=auctions).get()
            prev_bids = bid.objects.filter(auctioneer=auctions)
            if prev_bid_winning:
                if prev_bid_winning.user == request.user:
                    msg = "You are already wining this auction."
                    return render(request, "auction.html", {'auctioneer':auctions,'bb': prev_bids, 'msg': msg})

                if float(amount) - prev_bid_winning.amount < 1:
                    msg = "Bid has to be at atleast 1 greater than previous bids."
                    return render("auction.html", {'auctioneer':auctions,'bb': prev_bids, 'msg': msg})

                prev_bid_winning.is_winning = False
                prev_bid_winning.save()

            b = bid(user=request.user, amount=amount, auctioneer=auctions, is_winning=True)
            b.save()
            prev_bids = bid.objects.filter(auctioneer=auctions)
            msg = "Bid saved succesfully."

            return render(request, "auction.html", {'auctioneer':auctions,'bb':prev_bids, 'msg': msg})

        else:
            auctions = auction.objects.filter(id=id)
            if auctions:
                auctions = auction.objects.get(id=id)
            else:
                msg = "Auction not found"
                return render(request, "auction.html", {'msg': msg})

            b = bid.objects.filter(is_winning=True, auctioneer=auctions)
            if b:
                b = bid.objects.filter(is_winning=True, auctioneer=auctions).get()
            return render(request, "auction.html", {'auctioneer': auctions, 'bb': b})

        option = request.POST.get('option', '')
        if option == 'Yes':
            new_title = request.POST['title']
            new_description = request.POST['description']
            new_end_time = dateutil.parser.parse(request.POST.get('end_time'))
            new_base_price = request.POST['base_price']
            new_seller = request.user
            new_start_time = dateutil.parser.parse(request.POST.get('start_time'))
            new_location = request.POST.get('location')
            a = auction(title=new_title, description=new_description, end_time=new_end_time, base_price=new_base_price,
                        seller=new_seller, start_time=new_start_time, location=new_location)
            a.save()
            message = "New auction has been saved and a confirmation email has been sent to your email."
            return render('product_added.html', {'message': message})
        else:
            error = "Auction is not saved"
            form = createAuction()
            return render('add_auction.html', {'form': form, 'error': error})
    else:
        message = "You have to log in first"
        posts = auction.objects.all()
        return render(request, "home.html", {'msg': message, 'posts': posts})


def view_auction(request, id):
    auctioneer = auction.objects.filter(id=id)
    if auctioneer:
        auctioneer = auction.objects.get(id=id)
        bb = bid.objects.filter(is_winning=True, auctioneer=auctioneer)
        if bb:
            bb = bid.objects.filter(is_winning=True, auctioneer=auctioneer).get()
        prev_bids = bid.objects.filter(auctioneer=auctioneer)
        return render(request, "auction.html", {'auctioneer': auctioneer, 'bb': prev_bids})
    else:
        message = "Auction not found."
        posts = auction.objects.all()
        return render(request, "home.html", {'msg': message, 'posts': posts})


# def background_jobs():


def user_page(request):
    if request.user.is_authenticated:
        return render(request, 'user.html', {'user_id': request.user.id})
    else:
        return render(request, 'user.html')


class AuctionList(generics.ListAPIView):
    queryset = auction.objects.all()
    serializer_class = AuctionSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BidList(generics.ListAPIView):
    queryset = bid.objects.all()
    serializer_class = BidSerializer


class BidDetail(generics.ListAPIView):
    def get(self, request, id):
        specfic_bid = bid.objects.filter(auctioneer=id)
        data = BidSerializer(specfic_bid, many=True)
        return JsonResponse(data.data, safe=False)


class AuctionDetail(generics.RetrieveAPIView):
    queryset = auction.objects.all()
    serializer_class = AuctionSerializer

    # def get(self, request, id):
    #     specfic_product = auction.objects.filter(id=id)
    #     data = AuctionSerializer(specfic_product, many=True)
    #     return JsonResponse(data.data, safe=False)


