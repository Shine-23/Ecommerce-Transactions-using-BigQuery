from rest_framework.views import APIView
from api.bigquery_client import run_query
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Product, Transaction
from .serializers import CustomerSerializer, ProductSerializer, TransactionSerializer

class CustomerListView(APIView):
    def get(self, request):
        query = "SELECT * FROM `dsd-proj-444318.ecommerce_dataset.Customer` LIMIT 10"
        data = run_query(query)
        if data:
            return Response(data)
        else:
            return Response({"error": "Failed to fetch customer data"}, status=500)

class ProductListView(APIView):
    def get(self, request):
        query = "SELECT * FROM `dsd-proj-444318.ecommerce_dataset.Product` LIMIT 10"
        data = run_query(query)
        if data:
            return Response(data)
        else:
            return Response({"error": "Failed to fetch product data"}, status=500)

class TransactionListView(APIView):
    def get(self, request):
        query = "SELECT * FROM `dsd-proj-444318.ecommerce_dataset.Transactions` LIMIT 10"
        data = run_query(query)
        if data:
            return Response(data)
        else:
            return Response({"error": "Failed to fetch transaction data"}, status=500)
