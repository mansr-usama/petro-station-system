#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell -c "
from django.contrib.auth import get_user_model
from station.models import Fuel, Staff, Pump

User = get_user_model()
User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

if not Fuel.objects.exists():
    petrol = Fuel.objects.create(fuel_type='Petrol', price_per_litre=5300, current_stock=10000)
    diesel = Fuel.objects.create(fuel_type='Diesel', price_per_litre=4950, current_stock=8500)
    Pump.objects.create(pump_no='PUMP-01', fuel=petrol, current_quantity=5000)
    Pump.objects.create(pump_no='PUMP-02', fuel=diesel, current_quantity=4000)

if not Staff.objects.exists():
    Staff.objects.create(staff_name='Usama Mansoor', residence='Kampala', contact='0700000001', role='Manager', gender='Male')
    Staff.objects.create(staff_name='Sarah Namukasa', residence='Entebbe', contact='0700000002', role='Attendant', gender='Female')
"