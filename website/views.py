from django.shortcuts import render, redirect

from django.views import View
# Create your views here.

from .models import UserProjectDetails, Careers
from .serializers import UserProjectDetailsSerializer

from django.core.files.storage import FileSystemStorage

from djongo.database import connect

from utils.sheets_api import StorageSheets

from crossdash import settings

from bson.objectid import ObjectId

from datetime import datetime
import math
class Home(View):
    def get(self, request):
        client = connect("crossdash_website")
        services_list_obj = client.crossdash_website.data_lists.find_one({"name": "services_list"})

        services_list = services_list_obj.get("list")

        return render(request, 'website/index.html', {"services": services_list})

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

        return redirect("/")

class CareersView(View):
    def get(self, request):
        return render(request, "website/careers.html")

    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        post_applied = request.POST.get("post_applied")
        project_details = request.POST.get("project_details")
        job_type = request.POST.get("job_type")
        cv = request.FILES['cv'] if 'cv' in request.FILES else None

        if not cv:
            print(cv)
            return render(request, "website/careers.html", {'status': True, 'message': 'ThankYou for contacting'})

        id = math.floor(datetime.now().timestamp() * 1000)

        if not Careers.objects.filter(name=name,
                            email = email,
                            phone = phone,
                            post_applied= post_applied,
                            project_details = project_details,
                            job_type = job_type,):
            career = Careers.objects.create(
                name=name,
                email = email,
                phone = phone,
                post_applied= post_applied,
                project_details = project_details,
                job_type = job_type,
            )

        else:
            return render(request, "website/careers.html", {'statuc': False, 'message': 'Entry Already Exists'})
        career.id=id
        storage = FileSystemStorage(settings.MEDIA_ROOT)
        file = storage.save("careers/{}/cv.{}".format(str(career.id), cv.name.split('.')[-1]), cv)
        cv_url = storage.url(file)
        career.cv_url = cv_url
        career.save()

        data_list = [
            career.id,
            career.name,
            career.email,
            career.phone,
            career.post_applied,
            career.project_details,
            career.job_type,
            career.cv_url,
        ]

        sheet = StorageSheets(1)
        sheet.add_values(data_list)

        return render(request, "website/careers.html", {'statuc': True, 'message': 'ThankYou for contacting'})


class Projects(View):
    def get(self, request):
        return render(request, "website/projects.html")


class ProjectDetails(View):
    def get(self, request, id):
        return render(request, "website/qzzo-casestudy.html")
