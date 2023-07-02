from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from functools import wraps


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homepage')
        # if request.user.is_authenticated and request.user.groups.exists():
        #     group = request.user.groups.all()[0].name
        #     if group == 'admin':
        #         return redirect('newsletterPanel')
        #     else:
        #         return redirect('frontpage')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


#Grabi ni yasha alien kaayo
def customer_form_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if 'customer_form_data' in request.session:
            # Retrieve the form data from the session
            form_data = request.session.get('customer_form_data')
            name = form_data.get('name')
            reference_number = form_data.get('reference_number')

            # Check if the requested profile matches the form data
            if name == kwargs.get('profile_name'):
                return view_func(request, *args, **kwargs)

        # If the form data is not present or doesn't match the requested profile,
        # redirect to the customer input form page
        return redirect('customer-page')
    return _wrapped_view


