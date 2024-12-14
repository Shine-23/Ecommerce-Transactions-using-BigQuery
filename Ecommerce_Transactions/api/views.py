from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Product, Transaction
from .serializers import CustomerSerializer, ProductSerializer, TransactionSerializer

class CustomerListView(APIView):
    def get(self, request):
        query = "SELECT * FROM `savvy-cinema-444321-g4.dsd_project_data.customer` LIMIT 10"
        data = run_query(query)
        if data:
            return Response(data)
        else:
            return Response({"error": "Failed to fetch customer data"}, status=500)

class ProductListView(APIView):
    def get(self, request):
        query = "SELECT * FROM `savvy-cinema-444321-g4.dsd_project_data.product` LIMIT 10"
        data = run_query(query)
        if data:
            return Response(data)
        else:
            return Response({"error": "Failed to fetch product data"}, status=500)

class TransactionListView(APIView):
    def get(self, request):
        query = "SELECT * FROM `savvy-cinema-444321-g4.dsd_project_data.transaction` LIMIT 10"
        data = run_query(query)
        if data:
            return Response(data)
        else:
            return Response({"error": "Failed to fetch transaction data"}, status=500)
