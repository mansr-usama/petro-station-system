

from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

class Fuel(models.Model):
    fuel_type = models.CharField(max_length=50, unique=True)
    price_per_litre = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.fuel_type} (UGX {self.price_per_litre}/L)"


class Staff(models.Model):
    ROLE_CHOICES = [
        ("Attendant", "Attendant"),
        ("Cashier", "Cashier"),
        ("Manager", "Manager"),
        ("Supervisor", "Supervisor"),
    ]
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    staff_name = models.CharField(max_length=100)
    residence = models.CharField(max_length=100)
    contact = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^\d{10}$', 'Contact must be exactly 10 digits.')]
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.staff_name} ({self.role})"


class Pump(models.Model):
    pump_no = models.CharField(max_length=20, unique=True)
    fuel = models.ForeignKey(Fuel, on_delete=models.PROTECT)
    current_quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.pump_no} - {self.fuel.fuel_type}"


class ShiftAllocation(models.Model):
    SESSION_CHOICES = [
        ("Morning", "Morning"),
        ("Afternoon", "Afternoon"),
        ("Evening", "Evening"),
    ]

    pump = models.ForeignKey(Pump, on_delete=models.PROTECT)
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT)
    session = models.CharField(max_length=20, choices=SESSION_CHOICES)
    date = models.DateField()

    def __str__(self):
        return f"Shift {self.id}: {self.staff.staff_name} on {self.pump.pump_no} ({self.session})"


class Transaction(models.Model):
    date_time = models.DateTimeField()
    pump = models.ForeignKey(Pump, on_delete=models.PROTECT)
    quantity_litres = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    price_per_litre = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT)

    @property
    def total_amount(self):
        return self.quantity_litres * self.price_per_litre

    def __str__(self):
        return f"Transaction #{self.id} - {self.pump.pump_no}"


class StockDetail(models.Model):
    fuel = models.ForeignKey(Fuel, on_delete=models.PROTECT)
    open_stock = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity_sold = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateField()

    @property
    def closing_stock(self):
        return self.open_stock + self.quantity_received - self.quantity_sold

    @property
    def stock_status_alert(self):
        stock = self.closing_stock
        if stock > 2000:
            return f"STOCK LEVEL - {stock} - STILL HIGH"
        elif stock >= 500:
            return f"STOCK LEVEL - {stock} - STILL OK"
        else:
            return f"STOCK LEVEL - {stock} - VERY LOW - RESTOCK NOW!"

    def __str__(self):
        return f"Stock Record #{self.id} ({self.fuel.fuel_type} - {self.date})"


class Stocking(models.Model):
    fuel = models.ForeignKey(Fuel, on_delete=models.PROTECT)
    quantity_stocked = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateField()

    def __str__(self):
        return f"Restock #{self.id} ({self.fuel.fuel_type} - {self.quantity_stocked}L)"