from django.contrib import admin
from .models import Fuel, Staff, Pump, ShiftAllocation, Transaction, StockDetail, Stocking

admin.site.register(Fuel)
admin.site.register(Staff)
admin.site.register(Pump)
admin.site.register(ShiftAllocation)
admin.site.register(Transaction)
admin.site.register(StockDetail)
admin.site.register(Stocking)