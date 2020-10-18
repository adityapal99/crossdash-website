from django.shortcuts import render, redirect

from django.views import View
# Create your views here.

from .models import UserProjectDetails
from .serializers import UserProjectDetailsSerializer

from utils.sheets_api import StorageSheets

class Home(View):
    def get(self, request):
        return render(request, 'website/Home.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        service = request.POST.get('service')
        details = request.POST.get('details')

        details = UserProjectDetails.objects.get_or_create(first_name=first_name, last_name=last_name, email=email, phone=phone, service=service, details=details)
        serialized_data = UserProjectDetailsSerializer(details).data

        data_list = [
            serialized_data.get('id'),
            serialized_data.get('first_name'),
            serialized_data.get('last_name'),
            serialized_data.get('email'),
            serialized_data.get('phone'),
            serialized_data.get('service'),
            serialized_data.get('details'),
        ]
        sheet = StorageSheets(0)
        sheet.add_values(data_list)

        return render(request, 'website/Home.html')