from django.urls import path
from .views import CustomerCreateView, CustomerListView, CustomerDetailView, AdminProfileCreateView, AdminProfileListView, CustomerMeView

urlpatterns = [
    path("ADD", CustomerCreateView.as_view(), name="customer-create"),
    path("me", CustomerMeView.as_view(), name="customer-me"),
    path("get", CustomerListView.as_view(), name="customer-list"),
    path("getuser/<uuid:customer_id>", CustomerDetailView.as_view(), name="customer-detail"),
    path("admin/add", AdminProfileCreateView.as_view(), name="admin-create"),
    path("admin/getall", AdminProfileListView.as_view(), name="admin-list"),
]
