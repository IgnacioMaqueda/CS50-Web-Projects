from django.contrib import admin

# Register your models here.
from .models import User, Category, Listing, Bid, Comment, Watchlist

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "base_price", "current_price", "created_by", "category", "image", "datetime", "bids", "closed")
    

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
