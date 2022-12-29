from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives, mail_admins
from datetime import datetime as DT
from .models import Appointment
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)





# class AppointmentView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'make_appointment.html', {})
#
#     def post(self, request, *args, **kwargs):
#         appointment = Appointment(
#             date=DT.strptime(request.POST['date'], "%Y-%m-%d"),
#             client_name=request.POST['client_name'],
#             message=request.POST['message'],
#             email=request.POST['email']
#         )
#         appointment.save()
#
#         mail_admins(
#             subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%m-%d")}',
#             message=appointment.message,
#
#         )

class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=DT.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
            email=request.POST['email']
        )
        appointment.save()

        return redirect('make_appointment')
