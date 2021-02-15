from django.contrib import admin
from binanceApp.models import Order
# Register your models here.


@admin.register(Order)
class TradeHistoryAdmin(admin.ModelAdmin):
    list_display = ('order',  'range_price','btc_count', 'created')