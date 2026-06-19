from django.contrib import admin
from .models import Restaurant

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'region', 'user', 'rating_avg', 'created_at']
    list_filter = ['category', 'region', 'price_range']
    search_fields = ['name', 'address']
