from django.shortcuts import render, get_object_or_404
from .forms import CashInForm, CashOutForm
from django.db.models import Sum
from django.shortcuts import render, redirect
from .forms import CashInForm, CashOutForm, Profile
from .models import CashIn, CashOut, DailyRecord, MissionVision
from .utils import generate_daily_records
from datetime import date
from django.http import HttpResponse
from django.template.loader import render_to_string
from datetime import datetime
import pdfkit
import calendar
import matplotlib.pyplot as plt
import io
import base64
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import unauthenticated_user, customer_form_required


@login_required(login_url='login')
def CashInOut(request):
    auth_user = request.user
    cash_ins = CashIn.objects.all()  # Retrieve all CashIn objects from the database
    cash_outs = CashOut.objects.all()
    cash_out_form = CashOutForm()
    cash_in_form = CashInForm()
    # New, Separation of forms
    if request.method == 'POST':
        # <button class="post-btn" name="cash_in_form_submit" type="submit">Submit</button>
        # name of the button
        if 'cash_in_form_submit' in request.POST:
            cash_in_form = CashInForm(request.POST)
            if cash_in_form.is_valid():
                cash_in = cash_in_form.save(commit=False)
                cash_in.save()
        # <button class="post-btn" name="cash_out_form_submit" type="submit">Submit</button>
        # name of the button
        elif 'cash_out_form_submit' in request.POST:
            cash_out_form = CashOutForm(request.POST)
            if cash_out_form.is_valid():
                cash_out = cash_out_form.save(commit=False)
                cash_out.save()
    # EndNew

    # New
    total_cash_ins = CashIn.objects.aggregate(Sum('cash_in'))['cash_in__sum'] or 0
    total_cash_outs = CashOut.objects.aggregate(Sum('cash_out'))['cash_out__sum'] or 0
    # EndNew

    return render(request, 'base.html', {
        'cash_in_form': cash_in_form,
        'cash_out_form': cash_out_form,
        'cash_ins': cash_ins,
        'cash_outs': cash_outs,
        'total_cash_ins': total_cash_ins,
        'total_cash_outs': total_cash_outs,
        'auth_user': auth_user,
    })


@customer_form_required
def Customer_Profile(request, profile_name):
    customer_profile = get_object_or_404(Profile, profile_name=profile_name)
    cash_ins = CashIn.objects.filter(name=customer_profile)
    cash_outs = CashOut.objects.filter(name=customer_profile)

    return render(request, 'customer_profile.html', {
        'customer_profile': customer_profile,
        'cash_ins': cash_ins,
        'cash_outs': cash_outs,
    })


# def customer_input_form_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         reference_number = request.POST.get('reference_number')
#
#         try:
#             profile = get_object_or_404(Profile, profile_name=name)
#             cash_in = get_object_or_404(CashIn, name=profile, reference_no=reference_number)
#             cash_out = get_object_or_404(CashOut, name=profile, reference_no=reference_number)
#             # Store the form data in the session
#             request.session['customer_form_data'] = {
#                 'name': name,
#                 'reference_number': reference_number,
#             }
#
#             return redirect('customer_profile', profile_name=profile.profile_name)
#         except (Profile.DoesNotExist, CashIn.DoesNotExist, CashOut.DoesNotExist):
#             # If the profile or cash in with given reference number doesn't exist, handle the error here
#             pass
#
#     return render(request, 'customer_page.html')


def customer_input_form_view(request):
    mission_vision = MissionVision.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        reference_number = request.POST.get('reference_number')

        profile = get_object_or_404(Profile, profile_name=name)
        cash_in = CashIn.objects.filter(name=profile, reference_no=reference_number).first()
        cash_out = CashOut.objects.filter(name=profile, reference_no=reference_number).first()

        if cash_in or cash_out:
            # If either cash_in or cash_out object exists, store the form data in the session
            request.session['customer_form_data'] = {
                'name': name,
                'reference_number': reference_number,
            }
            return redirect('customer_profile', profile_name=profile.profile_name)
        else:
            # If neither cash_in nor cash_out objects are found, handle the error here or display a message
            pass

    return render(request, 'customer_page.html', {
        'mission_vision': mission_vision,
    })


@login_required(login_url='login')
def DailyRecords(request):
    # Get the selected date from the request parameters
    default_date = date.today()
    selected_date = request.GET.get('date')

    # Retrieve the daily record for the selected date
    daily_record = DailyRecord.objects.filter(date=selected_date).first()

    # Generate the daily records for the current date if it doesn't exist
    if not daily_record and selected_date == str(date.today()):
        daily_record = generate_daily_records()

    # Retrieve the cash-in and cash-out transactions for the selected date
    cash_ins = CashIn.objects.filter(date_added__date=selected_date)
    cash_outs = CashOut.objects.filter(date_added__date=selected_date)

    total_cash_ins = cash_ins.aggregate(total=Sum('cash_in'))['total'] or 0

    total_cash_outs = cash_outs.aggregate(total=Sum('cash_out'))['total'] or 0

    return render(request, 'daily_records.html', {
        'daily_record': daily_record,
        'cash_ins': cash_ins,
        'cash_outs': cash_outs,
        'total_cash_ins': total_cash_ins,
        'total_cash_outs': total_cash_outs,
        'selected_date': selected_date,
        'default_date': default_date,
    })


@login_required(login_url='login')
def monthly_records(request):
    default_date = date.today()
    if request.method == 'GET':
        selected_date = request.GET.get('selected_date')

        if selected_date:
            # Convert the selected date to a Python date object
            selected_date = datetime.strptime(selected_date + '-01', '%Y-%m-%d').date()
            selected_year = selected_date.year
            selected_month = selected_date.month

            selected_month_word = calendar.month_name[selected_month]

            # Get the cash-in and cash-out transactions for the selected year and month
            cash_ins = CashIn.objects.filter(date_added__year=selected_year, date_added__month=selected_month)
            cash_outs = CashOut.objects.filter(date_added__year=selected_year, date_added__month=selected_month)

            # Calculate the total cash-ins and cash-outs for the selected year and month
            total_cash_ins = cash_ins.aggregate(total=Sum('cash_in'))['total'] or 0
            total_cash_outs = cash_outs.aggregate(total=Sum('cash_out'))['total'] or 0

            # months = [calendar.month_name[i][:3] for i in range(1, 13)]
            # cash_in_totals = [cash_ins.filter(date_added__month=month).aggregate(total=Sum('cash_in'))['total'] or 0 for month in range(1, 13)]
            #
            # # Generating the Bar Graph
            # plt.figure(figsize=(10, 6))
            # plt.bar(months, cash_in_totals)
            # plt.xlabel('Months')
            # plt.ylabel('Total Cash-In')
            # plt.title('Monthly Total Cash-In')
            # plt.tight_layout()
            #
            # # Convert the plot to an image
            # buffer = io.BytesIO()
            # plt.savefig(buffer, format='png')
            # buffer.seek(0)
            # graph = base64.b64encode(buffer.read()).decode('utf-8')
            # plt.close()

            return render(request, 'monthy_records.html', {
                'selected_month_word': selected_month_word,
                'default_date': default_date,
                'selected_year': selected_year,
                'selected_month': selected_month,
                'total_cash_ins': total_cash_ins,
                'total_cash_outs': total_cash_outs,
                'cash_ins': cash_ins,
                'cash_outs': cash_outs,
            })

    # If the form is not submitted or no date is selected, display the template without filtering
    return render(request, 'monthy_records.html')


@login_required(login_url='login')
def yearly_records(request):
    current_year = date.today().year
    if request.method == 'GET':
        selected_date = request.GET.get('selected_date')

        if selected_date:
            # Convert the selected date to a Python date object
            selected_year = int(selected_date)

            # Get the cash-in and cash-out transactions for the selected year and month
            cash_ins = CashIn.objects.filter(date_added__year=selected_year)
            cash_outs = CashOut.objects.filter(date_added__year=selected_year)

            # Calculate the total cash-ins and cash-outs for the selected year and month
            total_cash_ins = cash_ins.aggregate(total=Sum('cash_in'))['total'] or 0
            total_cash_outs = cash_outs.aggregate(total=Sum('cash_out'))['total'] or 0

            return render(request, 'yearly_records.html', {
                'current_year': current_year,
                'selected_year': selected_year,
                'total_cash_ins': total_cash_ins,
                'total_cash_outs': total_cash_outs,
                'cash_ins': cash_ins,
                'cash_outs': cash_outs,
            })

    # If the form is not submitted or no date is selected, display the template without filtering
    return render(request, 'yearly_records.html')


def generate_pdf(request):
    # Get the selected date from the request parameters
    default_date = date.today()
    selected_date = request.GET.get('date')

    # Retrieve the daily record for the selected date
    daily_record = DailyRecord.objects.filter(date=selected_date).first()

    # Generate the daily records for the current date if it doesn't exist
    if not daily_record and selected_date == str(date.today()):
        daily_record = generate_daily_records()

    # Retrieve the cash-in and cash-out transactions for the selected date
    cash_ins = CashIn.objects.filter(date_added__date=selected_date)
    cash_outs = CashOut.objects.filter(date_added__date=selected_date)

    total_cash_ins = cash_ins.aggregate(total=Sum('cash_in'))['total'] or 0

    total_cash_outs = cash_outs.aggregate(total=Sum('cash_out'))['total'] or 0

    # Render the template as HTML
    html = render_to_string('print_template.html', {
        'selected_date': selected_date,
        'daily_record': daily_record,
        'cash_ins': cash_ins,
        'cash_outs': cash_outs,
        'total_cash_ins': total_cash_ins,
        'total_cash_outs': total_cash_outs,
    })

    # Generate PDF from the HTML content
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'quiet': '',
        'print-media-type': '',
        'disable-smart-shrinking': '',
        'no-outline': '',
    }

    # Set the path to wkhtmltopdf executable here
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

    # Generate the PDF
    pdf = pdfkit.from_string(html, False, options=options, configuration=config)

    # Create a response with PDF content to trigger download
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="daily_records.pdf"'
    return response


def generate_monthly_pdf(request):
    selected_date = request.GET.get('selected_date', None)

    if selected_date:
        selected_date = datetime.strptime(selected_date + '-01', '%Y-%m-%d').date()
        selected_year = selected_date.year
        selected_month = selected_date.month

        selected_month_word = calendar.month_name[selected_month]

    # Get the cash-in and cash-out transactions for the selected year and month
        cash_ins = CashIn.objects.filter(date_added__year=selected_year, date_added__month=selected_month)
        cash_outs = CashOut.objects.filter(date_added__year=selected_year, date_added__month=selected_month)

    # Calculate the total cash-ins and cash-outs for the selected year and month
        total_cash_ins = cash_ins.aggregate(total=Sum('cash_in'))['total'] or 0
        total_cash_outs = cash_outs.aggregate(total=Sum('cash_out'))['total'] or 0

    # Render the template as HTML
        html = render_to_string('monthly_report_print.html', {
            'selected_month_word': selected_month_word,
            'selected_year': selected_year,
            'selected_month': selected_month,
            'cash_ins': cash_ins,
            'cash_outs': cash_outs,
            'total_cash_ins': total_cash_ins,
            'total_cash_outs': total_cash_outs,
        })

    # Generate PDF from the HTML content
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'quiet': '',
        'print-media-type': '',
        'disable-smart-shrinking': '',
        'no-outline': '',
    }

    # Set the path to wkhtmltopdf executable here
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

    # Generate the PDF
    pdf = pdfkit.from_string(html, False, options=options, configuration=config)

    # Create a response with PDF content to trigger download
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="monthly_records.pdf"'
    return response


def generate_annual_pdf(request):
    current_year = date.today().year
    if request.method == 'GET':
        selected_date = request.GET.get('selected_date')

        if selected_date:
            # Convert the selected date to a Python date object
            selected_year = int(selected_date)

            # Get the cash-in and cash-out transactions for the selected year and month
            cash_ins = CashIn.objects.filter(date_added__year=selected_year)
            cash_outs = CashOut.objects.filter(date_added__year=selected_year)

            # Calculate the total cash-ins and cash-outs for the selected year and month
            total_cash_ins = cash_ins.aggregate(total=Sum('cash_in'))['total'] or 0
            total_cash_outs = cash_outs.aggregate(total=Sum('cash_out'))['total'] or 0

            html = render_to_string('annual_report_print.html', {
                'selected_year': selected_year,
                'cash_ins': cash_ins,
                'cash_outs': cash_outs,
                'total_cash_ins': total_cash_ins,
                'total_cash_outs': total_cash_outs,
            })

    # Generate PDF from the HTML content
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'quiet': '',
        'print-media-type': '',
        'disable-smart-shrinking': '',
        'no-outline': '',
    }

    # Set the path to wkhtmltopdf executable here
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

    # Generate the PDF
    pdf = pdfkit.from_string(html, False, options=options, configuration=config)

    # Create a response with PDF content to trigger download
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="annual_records.pdf"'
    return response


@unauthenticated_user
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.success(request, "Invalid form data. Please try again")

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


