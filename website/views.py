from django.shortcuts import render, redirect

from django.views import View
# Create your views here.

from .models import UserProjectDetails, Careers
from .serializers import UserProjectDetailsSerializer

from django.core.files.storage import FileSystemStorage

from utils.sheets_api import StorageSheets

from crossdash import settings

from bson.objectid import ObjectId

from datetime import datetime
import math
class Home(View):
    def get(self, request):
        return render(request, 'website/index.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        service = request.POST.get('service')
        details = request.POST.get('details')

        details = UserProjectDetails.objects.get_or_create(first_name=first_name, last_name=last_name, email=email, phone=phone, service=service, details=details)

        if not details[1]:
            return render(request, 'website/index.html')

        data_list = [
            details[0].id,
            details[0].first_name,
            details[0].last_name,
            details[0].email,
            details[0].phone,
            details[0].service,
            details[0].details,
        ]
        sheet = StorageSheets(0)
        sheet.add_values(data_list)

        return render(request, 'website/index.html')

class CareersView(View):
    def get(self, request):
        return render(request, "website/careers.html")

    def post(self, request):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        project_details = request.POST.get("project_details")
        job_type = request.POST.get("job_type")
        cv = request.FILES['cv'] if 'cv' in request.FILES else None

        if not cv:
            print(cv)
            return render(request, "website/careers.html", {'statuc': True, 'message': 'ThankYou for contacting'})

        id = math.floor(datetime.now().timestamp() * 1000)

        career = Careers.objects.get_or_create(
            id = id,
            first_name=first_name,
            last_name = last_name,
            email = email,
            phone = phone,
            project_details = project_details,
            job_type = job_type,
        )

        if not career[1]:
            return render(request, "website/careers.html", {'statuc': False, 'message': 'Entry Already Exists'})

        career = career[0]
        storage = FileSystemStorage(settings.MEDIA_ROOT)
        file = storage.save("careers/{}/cv.{}".format(str(career.id), cv.name.split('.')[-1]), cv)
        cv_url = storage.url(file)
        career.cv_url = cv_url
        career.save()

        data_list = [
            career.id,
            career.first_name,
            career.last_name,
            career.email,
            career.phone,
            career.project_details,
            career.job_type,
            career.cv_url,
        ]

        sheet = StorageSheets(1)
        sheet.add_values(data_list)

        return render(request, "website/careers.html", {'statuc': True, 'message': 'ThankYou for contacting'})

