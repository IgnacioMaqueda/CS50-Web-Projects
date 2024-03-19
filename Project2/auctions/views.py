from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Bid, Comment, Watchlist


def index(request):
    listings = Listing.objects.filter(closed=False)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "active": True
    })


def closed_listings(request):
    listings = Listing.objects.filter(closed=True)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "active": False
    })


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category(request, category_id):
    category = Category.objects.get(id=category_id)
    listings = Listing.objects.filter(category=category_id)
    return render(request, "auctions/index.html", {
        "category": category,
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def watchlist(request):
    watchlist_listings = Watchlist.objects.filter(user=request.user).values_list('listing', flat=True)
    listings = Listing.objects.filter(id__in=watchlist_listings)
    return render(request, "auctions/index.html", {
        "watchlist": request.user,
        "listings": listings
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        image = request.POST["image"]
        category = Category.objects.get(pk=int(request.POST["category"]))
        listing = Listing(title=title, description=description, base_price=price, current_price=price, image=image, category=category,
                          created_by=request.user, bids=0, closed=False)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        categories = Category.objects.all()
        return render(request, "auctions/createlisting.html", {
            "categories": categories
        })


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bids = Bid.objects.filter(listing=listing_id)
    comments = Comment.objects.filter(listing=listing_id)
    if request.user.is_authenticated:
        in_watchlist = Watchlist.objects.filter(listing=listing_id, user=request.user).exists()
    else:
        in_watchlist = False
    if bids:
        bid = bids.latest('price')
    else:
        bid = None
    if request.method == "POST":
        if 'bidding' in request.POST:
            bid_price = int(request.POST["price"])
            if bid_price > listing.current_price:
                listing.current_price = bid_price
                listing.bids += 1
                listing.save()
                bid = Bid(user=request.user, listing=listing, price=bid_price)
                bid.save()
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "bid": bid,
                    "comments": comments,
                    "message": "Bid too low.",
                    "in_watchlist": in_watchlist
                })
        elif 'closing' in request.POST:
            listing.closed = True
            listing.save()
        elif 'commenting' in request.POST:
            comment = Comment(user=request.user,
                              listing=listing, text=request.POST["text"])
            comment.save()
        elif 'adding' in request.POST:
            watchlist = Watchlist(user=request.user, listing=listing)
            watchlist.save()
            in_watchlist = True
        elif 'removing' in request.POST:
            watchlist = Watchlist.objects.get(
                user=request.user, listing=listing)
            watchlist.delete()
            in_watchlist = False
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid": bid,
        "comments": comments,
        "in_watchlist": in_watchlist
    })
