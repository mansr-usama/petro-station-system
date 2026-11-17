from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("", views.index_view, name="home"),

    # Main Navigation Pages (matching your HTML structure)
    path("registration/", views.registration_view, name="registration"),
    path("transactions/", views.transactions_view, name="transactions"),
    path("stock/", views.stock_view, name="stock"),
    path("shift-allocation/", views.shift_allocation_view, name="shift_allocation"),

    # Staff Edit / Delete
    path("staff/<int:id>/edit/", views.staff_edit, name="staff_edit"),
    path("staff/<int:id>/delete/", views.staff_delete, name="staff_delete"),

    # Fuel Edit / Delete
    path("fuel/<int:id>/edit/", views.fuel_edit, name="fuel_edit"),
    path("fuel/<int:id>/delete/", views.fuel_delete, name="fuel_delete"),

    # Pump Edit / Delete
    path("pump/<int:id>/edit/", views.pump_edit, name="pump_edit"),
    path("pump/<int:id>/delete/", views.pump_delete, name="pump_delete"),

    # Transaction Edit / Delete
    path("transactions/<int:id>/edit/", views.transaction_edit, name="transaction_edit"),
    path("transactions/<int:id>/delete/", views.transaction_delete, name="transaction_delete"),

    # StockDetail Edit / Delete
    path("stock-detail/<int:id>/edit/", views.stock_detail_edit, name="stock_detail_edit"),
    path("stock-detail/<int:id>/delete/", views.stock_detail_delete, name="stock_detail_delete"),

    # Stocking (Restock) Edit / Delete
    path("stocking/<int:id>/edit/", views.stocking_edit, name="stocking_edit"),
    path("stocking/<int:id>/delete/", views.stocking_delete, name="stocking_delete"),

    # Shift Edit / Delete
    path("shift/<int:id>/edit/", views.shift_edit, name="shift_edit"),
    path("shift/<int:id>/delete/", views.shift_delete, name="shift_delete"),
]