from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Product, Transaction
from .serializers import CustomerSerializer, ProductSerializer, TransactionSerializer

class CustomerListView(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class TransactionListView(APIView):
    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
