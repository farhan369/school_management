import pandas as pd

from celery import shared_task

from django.core.mail import EmailMessage
from django.utils import timezone
from django.conf import settings

from rest_framework import views

from academics import models as academics_models


# create a function to apply styles conditionally
def apply_color(value):
    '''
    Applies green background color for True and red for False
    '''
    if value == True:
        color = 'background-color: green'
    else:
        color = 'background-color: red'
    return color


@shared_task
def daily_attendance_email():
    """
    Generate an attendence report excel everyday and send it 
    to admin using gmail
    """
    # Get attendance data for today
    today = timezone.now().date()

    # retrives the attendance object where date is today and performs 
    # JOIN operation to retrieve related data for the user field 
    # in the Attendance model
    attendance_data = academics_models.Attendance.objects.filter(
        date=today).select_related('user')
    
    attendance_df = pd.DataFrame(list(attendance_data.values(
        'user__user__username', 'is_present')))
    
    attendance_df = attendance_df.rename(columns={
        'user__user__username': 'Name'})
    
    attendance_df = attendance_df.style.applymap(apply_color, subset = ['is_present'])
    # Create an Excel file from the DataFrame
    filename = 'attendance.xlsx'
    writer = pd.ExcelWriter(filename)
    attendance_df.to_excel(writer, index=False)
    writer.save()

    # Send email to admin with Excel file attachment
    email = EmailMessage(
        subject='Attendance Report for Today',
        body='Please find attached the attendance report for today.',
        from_email=settings.EMAIL_HOST_USER,
        to=[settings.RECIPIENT_ADDRESS],
    )

    email.attach_file(filename)
    email.send()



