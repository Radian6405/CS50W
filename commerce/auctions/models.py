from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    name = models.CharField(max_length=64)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Listings")

    def __str__(self):
        return f"(*{self.name}* by  {self.seller})"

class Bids(models.Model):
    amount = models.IntegerField()
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="Bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bids")

    def __str__(self):
        return f"${self.amount} for {self.listing} by {self.bidder}"

class Comments(models.Model):
    text = models.CharField(max_length="300")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comments")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="Comments")

    def __str__(self):
        return f"{self.commenter}'s comment for {self.Listings}: \n{self.text}"