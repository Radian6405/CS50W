from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    #displays open and closed listings as cards
    openlistings = AuctionListing.objects.filter(isClosed=False)
    closedlistings = AuctionListing.objects.filter(isClosed=True)
    return render(request, "auctions/index.html", {
        "openlistings": openlistings,
        "closedlistings": closedlistings
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

@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        #form to create a listing
        listing = AuctionListing(
            name = request.POST["title"],
            description = request.POST["description"],
            seller = request.user,
            startBid = request.POST["startbid"],
            image = request.POST["imgurl"]
        )
        listing.save()

        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/createlisting.html")

#@login_required(login_url='login')
def listing(request, id):
    if request.method == "POST":
        #updating database
        listing = AuctionListing.objects.get(pk=id)
        listing.isClosed=True
        listing.save()

        return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
    
    listing = AuctionListing.objects.get(pk=id)
    comments = Comments.objects.filter(listing=listing)

    #displaying closed listings
    if listing.isClosed:
      return render(request, "auctions/listingpage.html", {
        "listing": listing,
        "comments": comments
    })

    #displaying open listings
    watchidlist = Watchlist.objects.filter(listing=listing).values_list("user")
    watchlist = []
    for i in watchidlist:
        watchlist.append(User.objects.get(pk=i[0]))        
    inWatchlist = request.user in watchlist

    return render(request, "auctions/listingpage.html", {
        "listing": listing,
        "inWatchlist": inWatchlist,
        "comments": comments
    })
    
@login_required(login_url='login')
def watchlist(request):
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=request.POST.get("listing"))
        watchidlist = Watchlist.objects.filter(listing=listing).values_list("user")
        watchlist = []
        for i in watchidlist:
            watchlist.append(User.objects.get(pk=i[0]))

        #adding/deleteing listing form user's watchlist
        if request.user in watchlist:
            Watchlist.objects.filter(user=request.user, listing=listing).delete()
        else:
            w = Watchlist(user=request.user, listing=listing)
            w.save()
        
        return HttpResponseRedirect(reverse("watchlist"))
    
    #displaying user's watchlist elements
    idlist = Watchlist.objects.filter(user=request.user).values_list("listing", flat=True)
    itemlist = []
    for i in idlist:
        itemlist.append(AuctionListing.objects.get(pk=i))

    return render(request, "auctions/watchlist.html", {
        "watchlist": itemlist
    })

@login_required(login_url='login')
def comment(request):
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=request.POST.get("userID"))
        comment = Comments(
            text=request.POST.get("text"),
            commenter=request.user,
            listing=listing
            )
        comment.save()
        return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
    return render(request, "auctions/pagenotfound.html")
