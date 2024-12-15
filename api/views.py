from rest_framework.views import APIView
from api.bigquery_client import query_with_retry
from rest_framework.response import Response

import os
from django.http import JsonResponse


class CustomerListView(APIView):
    def get(self, request):
        query = "SELECT * FROM `dsd-proj-444318.ecommerce_dataset.Customer` LIMIT 100"
        data = query_with_retry(query)
        if data:
            return Response(data)
        else:
            return Response({"error": "Failed to fetch customer data"}, status=500)

class ProductListView(APIView):
    def get(self, request):
        query = "SELECT * FROM `dsd-proj-444318.ecommerce_dataset.Product` LIMIT 100"
        data = query_with_retry(query)
        if data:
            return Response(data)
        else:
            return Response({"error": "Failed to fetch product data"}, status=500)

class TransactionListView(APIView):
    def get(self, request):
        query = "SELECT * FROM `dsd-proj-444318.ecommerce_dataset.Transactions` LIMIT 100"
        data = query_with_retry(query)
        if data:
            return Response(data)
        else:
            return Response({"error": "Failed to fetch transaction data"}, status=500)
        
class ClickStreamListView(APIView):
    def get(self, request):
        query = "SELECT * FROM `dsd-proj-444318.ecommerce_dataset.Click_Stream` LIMIT 100"
        data = query_with_retry(query)
        if data:
            return Response(data)
        else:
            return Response({"error": "Failed to fetch transaction data"}, status=500)
def shutdown_service(request):
    try:
        # Find the process using port 8000
        result = os.popen('netstat -ano | findstr :8000').read()
        lines = result.strip().split('\n')
        for line in lines:
            if "LISTENING" in line:
                pid = line.split()[-1]  # Extract the PID (last column)
                os.system(f"taskkill /F /PID {pid}")  # Kill the specific process
                return JsonResponse({"message": "Service on port 8000 stopped successfully"})

        return JsonResponse({"error": "No service found on port 8000"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
