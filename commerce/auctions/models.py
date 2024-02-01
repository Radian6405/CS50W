from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Listings")
    startBid = models.IntegerField()
    image = models.CharField(max_length=2048 ,null = True)
    isClosed = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="WinListings", null=True)

    def __str__(self):
        return f"(*{self.name}* by  {self.seller})"

class Bids(models.Model):
    amount = models.IntegerField()
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="Bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bids")

    def __str__(self):
        return f"${self.amount} for {self.listing} by {self.bidder}"

class Comments(models.Model):
    text = models.CharField(max_length=300)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comments")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="Comments")

    def __str__(self):
        return f"{self.commenter}'s comment for {self.listing}: \n{self.text}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Watchlist")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="Watchlist")

    def __str__(self):
        return f"{self.user}: {self.listing.name}"

class Categories(models.Model):
    class CATEGORIES(models.TextChoices):
        ANTIQUES = "AN", _("Antiques")
        ART = "AR", _("Art & Decor")
        BOOKS = "BO", _("Books")
        GAMES = "CD", _("CD, DVD & Games")
        CLOTHING = "CL", _("Clothing & Fasion")
        COLLECTABLES = "CO", _("Collectables")
        COMPUTERS = "CM", _("Computers")
        DINING = "DI", _("Dining")
        ELECTRONICS = "EL", _("Electronics & Gadgets")
        HANDBAGS = "HA", _("Handbags")
        LAWN = "LA", _("Lawn & Garden")
        SPORTS = "SP", _("Sports & Equipment")
        TOYS = "TO", _("Toys")
        TRAVEL = "TR", _("Travel Accesaries")

    category = models.CharField(max_length=2, choices=CATEGORIES, null=True)
    listing = models.ManyToManyField(AuctionListing, blank=True, related_name="Category")
    
    def __str__(self):
        return f"{self.category}"