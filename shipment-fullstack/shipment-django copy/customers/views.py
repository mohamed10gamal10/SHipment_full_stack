from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from .models import Customer, AdminProfile
from .serializers import CustomerSerializer, AdminProfileSerializer
from .permissions import IsAdminRole, IsCustomerRole
from .services import get_customer, create_customer

class CustomerCreateView(generics.CreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsCustomerRole]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if Customer.objects.filter(user=request.user).exists():
            raise PermissionDenied("Customer profile already exists.")
        customer = create_customer(request.user, serializer.validated_data)
        # Return the saved profile (with id) so the frontend can use it right away.
        return Response(CustomerSerializer(customer).data, status=201)

class CustomerMeView(APIView):
    """Current user's own customer profile. 404 if it has not been created yet."""
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        customer = Customer.objects.filter(user=request.user).first()
        if customer is None:
            return Response({"detail": "Customer profile not found."}, status=404)
        return Response(CustomerSerializer(customer).data)

class CustomerListView(generics.ListAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminRole]
    queryset = Customer.objects.all().order_by("-created_at")

class CustomerDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, customer_id):
        customer = get_customer(customer_id)
        if request.user.role != "admin" and customer.user_id != request.user.id:
            raise PermissionDenied("You can only view your own profile.")
        return Response(CustomerSerializer(customer).data)

class AdminProfileCreateView(generics.CreateAPIView):
    serializer_class = AdminProfileSerializer
    permission_classes = [IsAdminRole]

class AdminProfileListView(generics.ListAPIView):
    serializer_class = AdminProfileSerializer
    permission_classes = [IsAdminRole]
    queryset = AdminProfile.objects.all()
