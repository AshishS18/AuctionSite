from django.shortcuts import render
from .models import auction
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreateForm, createAuction, confAuction
import datetime
import dateutil.parser
from .serializers import AuctionSerializer, BidSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework import generics, filters
from .models import User, auction, bid


def home(request):
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
                    message = "Log in succesfull"
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
            new_user = form.save()

            posts = auction.objects.all()
            message = "New User is created. Please Login"
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
            form = createAuction(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                title = cd['title']
                description = cd['description']
                end_time = cd['end_time']
                base_price = cd['base_price']
                start_time = cd['start_time']
                location = cd['location']
                seller = request.user
                a = auction(title=title, description=description, end_time=end_time,
                            base_price=base_price, seller=seller, start_time=start_time,
                            location=location)
                a.save()
                # d = datetime.datetime.strptime(end_time, "%d/%m/%Y %H:%M:%S")
                #
                # if (d - datetime.datetime.now()).total_seconds() < 86400:
                #     message = "The minimum duration of an auction is 24hours. You have to change the deadline."
                #     form = createAuction()
                #     return render(request, 'add_auction.html', {'msg': message, 'form': form})

                # form = confAuction()
                # return render(request, 'confirm_auction.html', {'form': form, "title": title, "description": description, "end_time": end_time, "base_price": base_price, "start_time": start_time, "location": location})

                message = "New auction has been saved"
                return render(request, 'product_added.html', {'message': message})

            else:
                form = createAuction()
                return render(request, 'add_auction.html', {'form': form, "error": "Not valid data"},
                              )
    else:
        message = "You have to log in first"
        posts = auction.objects.all()
        return render(request, "home.html", {'msg': message, 'posts': posts})


def save_auction(request):
    if request.user.is_authenticated:
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
            # send_mail('New auction created.', "Your new auction has been created successfully.", 'no_repli@yaas.com', [request.user.email,], fail_silently=False)
            message = "New auction has been saved and a confirmation email has been sent to your email."
            return render('product_added.html', {'message': message})
        else:
            error = "Auction is not saved"
            form = createAuction()
            return render('add_auction.html', {'form': form, 'error': error})
    else:
        message = "You have to log in first"
        posts = auction.objects.all()
        return render("home.html", {'msg': message, 'posts': posts})


class AuctionList(generics.ListAPIView):
    queryset = auction.objects.all()
    serializer_class = AuctionSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BidList(generics.ListAPIView):
    queryset = bid.objects.all()
    serializer_class = BidSerializer
