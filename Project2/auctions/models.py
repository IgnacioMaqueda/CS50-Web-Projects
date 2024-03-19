from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_listings")
    image = models.URLField()
    datetime = models.DateTimeField(auto_now_add=True)
    bids = models.IntegerField()
    closed = models.BooleanField()

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user}: {self.price}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    text = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.user}: A comment"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_watchlist")

    def __str__(self):
        return f"{self.user}: {self.listing}"
