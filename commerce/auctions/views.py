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
        listingCategory = Categories.objects.filter(category = request.POST["category"]).first()

        if request.POST["category"] in Categories.CATEGORIES:
            listing.Category.add(listingCategory)
            listing.save()

        return HttpResponseRedirect(reverse("index"))
    
    categoryList = list(Categories.objects.all())
    categories = []
    for i in range(len(categoryList)):
        categories.append([str(categoryList[i]), categoryList[i].get_category_display()])
    return render(request, "auctions/createlisting.html", {
        "categorylist": categories,
    })

#@login_required(login_url='login')
def listing(request, id):
    #closing a listing
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=id)
        bids = Bids.objects.filter(listing=listing)
        winBid = listing.startBid
        for bid in bids:
            if winBid < bid.amount:
                winBid = bid.amount
                winner = bid.bidder
            
                
        if len(bids) == 0:
            listing.isClosed = True
        else:
            listing.isClosed = True
            listing.winner = winner

        listing.save()

        return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
    
    listing = AuctionListing.objects.get(pk=id)
    comments = Comments.objects.filter(listing=listing)
    bids = Bids.objects.filter(listing=listing).values_list("amount", flat=True)
    if len(bids) != 0:
        max_bid = max(bids)
    else:
        max_bid = 0
    categoryList = list(listing.Category.all())
    categories = []
    for i in range(len(categoryList)):
        categories.append([str(categoryList[i]), categoryList[i].get_category_display()])

    #displaying closed listings
    if listing.isClosed:
      return render(request, "auctions/listingpage.html", {
        "listing": listing,
        "comments": comments,
        "maxbid": f"${max_bid}" if max_bid > listing.startBid else "None",
        "categoryList": categories
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
        "comments": comments,
        "maxbid": f"${max_bid}" if max_bid > listing.startBid else "None",
        "categoryList": categories
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

@login_required(login_url='login')
def bid(request):
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=request.POST.get("userID"))
        amount = int(request.POST.get("amount"))

        bids = Bids.objects.filter(listing=listing).values_list("amount", flat=True)
        if len(bids) != 0:
            max_bid = max(bids)
        else:
            max_bid = 0

        if amount > max_bid and amount > listing.startBid:
            Bid = Bids(amount=amount, bidder=request.user, listing=listing)
            Bid.save()
            return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
        else:
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
            comments = Comments.objects.filter(listing=listing)

            return render(request, "auctions/listingpage.html", {
                "listing": listing,
                "inWatchlist": inWatchlist,
                "comments": comments,
                "message": f"Bid must be higher than {max_bid if max_bid > listing.startBid else listing.startBid}",
                "maxbid": f"${max_bid}" if max_bid > listing.startBid else "None"
            })

    return render(request, "auctions/pagenotfound.html")

def categories(request):
    categoryList = list(Categories.objects.all())
    categories = []
    for i in range(len(categoryList)):
        categories.append([str(categoryList[i]), categoryList[i].get_category_display()])
    return render(request, "auctions/categories.html", {
        "categorylist": categories
    })

def categoryPage(request, name):
    if not (name in Categories.CATEGORIES):
        return render(request, "auctions/pagenotfound.html")

    category = Categories.objects.filter(category=name).get()
    openlistings = category.listing.filter(isClosed=False)
    closedlistings = category.listing.filter(isClosed=True)

    return render(request, "auctions/index.html", {
        "openlistings": openlistings,
        "closedlistings": closedlistings,
    })
