from django.contrib import admin
from .models import Customer, Delivery, AdminProfile
admin.site.register(Customer)
admin.site.register(Delivery)
admin.site.register(AdminProfile)
