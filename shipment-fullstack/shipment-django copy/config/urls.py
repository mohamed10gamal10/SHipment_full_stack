from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("accounts.urls")),
    path("Customer/", include("customers.urls")),
    path("Admin/", include("customers.admin_urls")),
    path("Shipment/", include("shipments.urls")),
]
