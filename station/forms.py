from django import forms
from .models import Fuel, Staff, Pump, ShiftAllocation, Transaction, StockDetail, Stocking

class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

class StaffForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Staff
        fields = "__all__"

class FuelForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Fuel
        fields = "__all__"

class PumpForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Pump
        fields = "__all__"

class ShiftAllocationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ShiftAllocation
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

class TransactionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Transaction
        fields = "__all__"
        widgets = {
            "date_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

class StockDetailForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = StockDetail
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        open_stock = cleaned_data.get("open_stock") or 0
        received = cleaned_data.get("quantity_received") or 0
        sold = cleaned_data.get("quantity_sold") or 0
        if (open_stock + received - sold) < 0:
            raise forms.ValidationError("Quantity sold is more than the stock available.")
        return cleaned_data

class StockingForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Stocking
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
