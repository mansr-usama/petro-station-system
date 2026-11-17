from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Fuel, Staff, Pump, ShiftAllocation, Transaction, StockDetail, Stocking
from .forms import (
    StaffForm, FuelForm, PumpForm, ShiftAllocationForm,
    TransactionForm, StockDetailForm, StockingForm
)

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "station/signup.html", {"form": form})


def index_view(request):
    context = {
        "staff_count": Staff.objects.count(),
        "fuel_count": Fuel.objects.count(),
        "pump_count": Pump.objects.count(),
        "transaction_count": Transaction.objects.count(),
    }
    return render(request, "station/index.html", context)


# 1. REGISTRATION PAGE (Staff, Fuel, Pump combined just like your HTML)
@login_required
def registration_view(request):
    staff_form = StaffForm()
    fuel_form = FuelForm()
    pump_form = PumpForm()

    if request.method == "POST":
        if "submit_staff" in request.POST:
            staff_form = StaffForm(request.POST)
            if staff_form.is_valid():
                staff_form.save()
                messages.success(request, "Staff registered successfully.")
                return redirect("registration")
        elif "submit_fuel" in request.POST:
            fuel_form = FuelForm(request.POST)
            if fuel_form.is_valid():
                fuel_form.save()
                messages.success(request, "Fuel registered successfully.")
                return redirect("registration")
        elif "submit_pump" in request.POST:
            pump_form = PumpForm(request.POST)
            if pump_form.is_valid():
                pump_form.save()
                messages.success(request, "Pump registered successfully.")
                return redirect("registration")

    context = {
        "staff_form": staff_form,
        "fuel_form": fuel_form,
        "pump_form": pump_form,
        "staff_list": Staff.objects.all().order_by("id"),
        "fuel_list": Fuel.objects.all().order_by("id"),
        "pump_list": Pump.objects.select_related("fuel").all().order_by("id"),
    }
    return render(request, "station/registration_page.html", context)


# 2. TRANSACTIONS PAGE
@login_required
def transactions_view(request):
    form = TransactionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        tx = form.save()
        messages.success(request, f"Transaction added. Total amount: {tx.total_amount}")
        return redirect("transactions")

    transactions = Transaction.objects.select_related("pump", "staff").all().order_by("-id")
    total_sales = sum(t.total_amount for t in transactions)

    return render(request, "station/transactions.html", {
        "form": form,
        "transactions": transactions,
        "total_sales": total_sales,
    })


# 3. STOCK & RESTOCKING PAGE
@login_required
def stock_view(request):
    stock_detail_form = StockDetailForm()
    stocking_form = StockingForm()

    if request.method == "POST":
        if "submit_stock_detail" in request.POST:
            stock_detail_form = StockDetailForm(request.POST)
            if stock_detail_form.is_valid():
                stock_detail_form.save()
                messages.success(request, "Daily stock record added.")
                return redirect("stock")
        elif "submit_stocking" in request.POST:
            stocking_form = StockingForm(request.POST)
            if stocking_form.is_valid():
                stocking_form.save()
                messages.success(request, "Restock record added.")
                return redirect("stock")

    context = {
        "stock_detail_form": stock_detail_form,
        "stocking_form": stocking_form,
        "stock_details": StockDetail.objects.select_related("fuel").all().order_by("-id"),
        "stockings": Stocking.objects.select_related("fuel").all().order_by("-id"),
    }
    return render(request, "station/stock.html", context)


# 4. SHIFT ALLOCATION PAGE
@login_required
def shift_allocation_view(request):
    form = ShiftAllocationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Shift allocated successfully.")
        return redirect("shift_allocation")

    shifts = ShiftAllocation.objects.select_related("pump", "staff").all().order_by("-id")
    return render(request, "station/shift_allocation.html", {
        "form": form,
        "shifts": shifts,
    })


# --- GENERIC EDIT & DELETE HELPERS ---
def _handle_edit(request, model_cls, form_cls, id, heading, back_url):
    record = get_object_or_404(model_cls, id=id)
    form = form_cls(request.POST or None, instance=record)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{heading} updated.")
        return redirect(back_url)
    return render(request, "station/form.html", {"form": form, "heading": heading, "back_url": back_url})

def _handle_delete(request, model_cls, id, heading, back_url):
    record = get_object_or_404(model_cls, id=id)
    if request.method == "POST":
        record.delete()
        messages.success(request, f"{heading} deleted.")
        return redirect(back_url)
    return render(request, "station/confirm_delete.html", {"record": record, "heading": heading, "back_url": back_url})


# EDIT & DELETE VIEWS FOR ALL 7 MODELS
@login_required
def staff_edit(request, id): return _handle_edit(request, Staff, StaffForm, id, "Edit Staff", "registration")
@login_required
def staff_delete(request, id): return _handle_delete(request, Staff, id, "Delete Staff", "registration")

@login_required
def fuel_edit(request, id): return _handle_edit(request, Fuel, FuelForm, id, "Edit Fuel", "registration")
@login_required
def fuel_delete(request, id): return _handle_delete(request, Fuel, id, "Delete Fuel", "registration")

@login_required
def pump_edit(request, id): return _handle_edit(request, Pump, PumpForm, id, "Edit Pump", "registration")
@login_required
def pump_delete(request, id): return _handle_delete(request, Pump, id, "Delete Pump", "registration")

@login_required
def transaction_edit(request, id): return _handle_edit(request, Transaction, TransactionForm, id, "Edit Transaction", "transactions")
@login_required
def transaction_delete(request, id): return _handle_delete(request, Transaction, id, "Delete Transaction", "transactions")

@login_required
def stock_detail_edit(request, id): return _handle_edit(request, StockDetail, StockDetailForm, id, "Edit Stock Record", "stock")
@login_required
def stock_detail_delete(request, id): return _handle_delete(request, StockDetail, id, "Delete Stock Record", "stock")

@login_required
def stocking_edit(request, id): return _handle_edit(request, Stocking, StockingForm, id, "Edit Restock Record", "stock")
@login_required
def stocking_delete(request, id): return _handle_delete(request, Stocking, id, "Delete Restock Record", "stock")

@login_required
def shift_edit(request, id): return _handle_edit(request, ShiftAllocation, ShiftAllocationForm, id, "Edit Shift Allocation", "shift_allocation")
@login_required
def shift_delete(request, id): return _handle_delete(request, ShiftAllocation, id, "Delete Shift Allocation", "shift_allocation")