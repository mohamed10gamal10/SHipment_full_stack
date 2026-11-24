from django.core.cache import cache
from rest_framework.exceptions import NotFound
from .models import Customer

def get_customer(customer_id):
    cache_key = f"customer:{customer_id}"
    customer = cache.get(cache_key)
    if customer is None:
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise NotFound("Customer not found.")
        cache.set(cache_key, customer, timeout=300)
    return customer

def create_customer(user, validated_data):
    customer = Customer.objects.create(user=user, email=user.email, **validated_data)
    cache.delete(f"customer:{customer.pk}")
    return customer
