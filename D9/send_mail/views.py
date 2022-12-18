from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import send_mail
from datetime import datetime as DT
from .models import Appointment
from dotenv import load_dotenv
import os
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'send_mail:make_appointment', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=DT.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
            email=request.POST['email']
        )
        appointment.save()
        send_mail(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d.%m.%Y")}',
            message=appointment.message,
            from_email=str(os.getenv('FROM_EMAIL')),
            recipient_list=[str(appointment.email)]
        )
        return redirect('send_mail:make_appointment')

# Create your views here.