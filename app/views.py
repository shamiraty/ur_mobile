from django.shortcuts import render, redirect
from .forms import PersonForm,PersonFormReset
from django.db import models
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

def superuser_required(user):
    return user.is_superuser


@login_required
def person_create_view(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            # Save the form but do not commit yet
            person = form.save(commit=False)
            # Assign the logged-in user to the 'user' field
            person.user = request.user
            # Now save the Person instance
            person.save()
            # Display success message
            messages.success(request, 'Registration successful!')
            return redirect('create_person')  # Redirect back to the home page or the same form page
    else:
        form = PersonForm()

    return render(request, 'home.html', {'form': form})

from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import PersonFormReset

@login_required
def person_create_reset_view(request):
    if request.method == 'POST':
        form = PersonFormReset(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            # Save the form but do not commit yet
            person = form.save(commit=False)
            # Assign the logged-in user to the 'user' field
            person.user = request.user
            # Now save the Person instance
            person.save()
            # Display success message
            messages.success(request, 'Registration successful!')
            return redirect('create_person_reset')  # Redirect back to the home page or the same form page
    else:
        form = PersonFormReset()

    return render(request, 'homereset.html', {'form': form})




from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from .models import *

@login_required
def payroll_employee_list(request):
    # Get start_date and end_date from request parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Get status filter from request parameters
    status_true = 'status_true' in request.GET
    status_false = 'status_false' in request.GET
    status_all = 'status_all' in request.GET

    # Fetch the logged-in user's district and post
    user = request.user
    try:
        employee = user.employee  # Assumes a OneToOne relation with Employee
        user_district = employee.district
    except Employee.DoesNotExist:
        user_district = None

    # If user_district is not found, we could return a message or redirect
    if not user_district:
        return render(request, 'error.html', {'message': 'User district not found'})

    # Get the branch of the user's district
    user_branch = user_district.branch

    # Fetch all districts in the same branch as the user's district
    districts_in_user_branch = District.objects.filter(branch=user_branch)

    # Filter Payroll records based on dates or return all Payrolls if no dates provided
    payrolls = Payroll.objects.all()  # Fallback to all records if no date range is provided

    # Get check numbers from filtered Payroll records
    payroll_check_numbers = payrolls.values_list('checkNumber', flat=True)

    # Fetch Persons with check_number in payroll_check_numbers and filter by date range
    if start_date and end_date:
        persons = Person.objects.filter(
            check_number__in=payroll_check_numbers,
            registered_date__range=[start_date, end_date]
        )
    else:
        persons = Person.objects.filter(check_number__in=payroll_check_numbers)

    # Apply status filtering
    if status_all:
        pass
    elif status_true:
        persons = persons.filter(status=True)
    elif status_false or not (status_true or status_all):
        persons = persons.filter(status=False)

    # Check if the user is a superuser
    if user.is_superuser:
        # For superusers, do not filter by district
        pass
    else:
        # Filter persons by district for non-superusers
        persons = persons.filter(
            user__employee__district__in=districts_in_user_branch
        )

    # Create a list of dictionaries to merge both Person and Payroll data
    data = []
    for person in persons:
        try:
            payroll = payrolls.get(checkNumber=person.check_number)
            data.append({
                'check_number': person.check_number,
                'fname': payroll.fname,
                'mname': payroll.mname,
                'lname': payroll.lname,
                'bankName': payroll.bankName,
                'accountNumber': payroll.accountNumber,
                'grossAmount': payroll.grossAmount,
                'basicSalary': payroll.basicSalary,
                'netAmount': payroll.netAmount,
                'allowance': payroll.allowance,
                'department': payroll.department,
                'simu': person.simu,
                'status': person.status,
                'image': person.image,
                'username': person.user.username,  # Corrected here
            })
        except Payroll.DoesNotExist:
            continue

    # Count records based on status
    total_count = persons.count()
    false_count = persons.filter(status=False).count()
    true_count = persons.filter(status=True).count()

    context = {
        'data': data,
        'start_date': start_date,
        'end_date': end_date,
        'total_count': total_count,
        'false_count': false_count,
        'true_count': true_count,
    }
    return render(request, 'person_list.html', context)








from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Person, PersonReset

#@user_passes_test(superuser_required, login_url='welcome')  # Redirect non-superusers to welcome page
@login_required
def update_status(request, check_number):
    if not request.user.is_authenticated:  # Check user authentication
        return HttpResponseForbidden("You are not authorized to perform this action.")
    
    person = get_object_or_404(Person, check_number=check_number)
    
    if request.method == 'POST':
        # Toggle status
        person.status = not person.status
        person.save()
    
    return redirect('person_list')  # Redirect to a view that shows the updated list



















@login_required

def payroll_employee_list_reset(request):
    # Get start_date and end_date from request parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Get status filter from request parameters
    status_true = 'status_true' in request.GET
    status_false = 'status_false' in request.GET
    status_all = 'status_all' in request.GET

    # Fetch the logged-in user's district
    user = request.user
    try:
        employee = user.employee  # Assumes a OneToOne relation with Employee
        user_district = employee.district
    except Employee.DoesNotExist:
        user_district = None

    # If user_district is not found, we could return a message or redirect
    if not user_district:
        return render(request, 'error.html', {'message': 'User district not found'})

    # Get the branch of the user's district
    user_branch = user_district.branch

    # Fetch all districts in the same branch as the user's district
    districts_in_user_branch = District.objects.filter(branch=user_branch)

    # Filter Payroll records based on dates or return all Payrolls if no dates provided
    payrolls = Payroll.objects.all()  # Fallback to all records if no date range is provided

    # Get check numbers from filtered Payroll records
    payroll_check_numbers = payrolls.values_list('checkNumber', flat=True)

    # Fetch PersonsReset with check_number in payroll_check_numbers and filter by date range
    if start_date and end_date:
        persons = PersonReset.objects.filter(
            check_number__in=payroll_check_numbers,
            registered_date__range=[start_date, end_date]
        )
    else:
        persons = PersonReset.objects.filter(check_number__in=payroll_check_numbers)

    # Apply status filtering
    if status_all:
        pass
    elif status_true:
        persons = persons.filter(status=True)
    elif status_false or not (status_true or status_all):  # Default to False if no filter selected
        persons = persons.filter(status=False)

    # Check if the user is a superuser
    if user.is_superuser:
        # For superusers, do not filter by district
        pass
    else:
        # Filter persons by district for non-superusers
        persons = persons.filter(
            user__employee__district__in=districts_in_user_branch
        )

    # Create a list of dictionaries to merge both PersonReset and Payroll data
    data = []
    for person in persons:
        try:
            payroll = payrolls.get(checkNumber=person.check_number)
            data.append({
                'check_number': person.id,
                'check_number_og': person.check_number,
                'fname': payroll.fname,
                'mname': payroll.mname,
                'lname': payroll.lname,
                'bankName': payroll.bankName,
                'accountNumber': payroll.accountNumber,
                'grossAmount': payroll.grossAmount,
                'basicSalary': payroll.basicSalary,
                'netAmount': payroll.netAmount,
                'allowance': payroll.allowance,
                'department': payroll.department,
                'simu': person.simu,
                'status': person.status,
                'image': person.image,
                'username': person.user.username,  # Corrected here
            })
        except Payroll.DoesNotExist:
            continue

    # Count records based on status
    total_count = persons.count()
    false_count = persons.filter(status=False).count()
    true_count = persons.filter(status=True).count()

    context = {
        'data': data,
        'start_date': start_date,  # Pass raw value to the template
        'end_date': end_date,      # Pass raw value to the template
        'total_count': total_count,
        'false_count': false_count,
        'true_count': true_count,
    }
    return render(request, 'person_list_reset.html', context)



@login_required
#@user_passes_test(superuser_required, login_url='welcome')  # Redirect non-superusers to welcome page
def update_status_reset(request, check_number):
    if not request.user.is_authenticated:  # Check user authentication
        return HttpResponseForbidden("You are not authorized to perform this action.")
    
    person = get_object_or_404(PersonReset, id=check_number)
    
    if request.method == 'POST':
        # Toggle status
        person.status = not person.status
        person.save()
    
    return redirect('person_list_reset')  # Redirect to a view that shows the updated list

@login_required
def welcome(request):
    return render(request,'welcome.html')




#send Message
from django.shortcuts import render, redirect
from django.contrib import messages  # Import messages framework
from .forms import MessageLogForm
def create_message_log(request):
    if request.method == 'POST':
        form = MessageLogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('contact')  # Reload the form page after success
    else:
        form = MessageLogForm()
    
    return render(request, 'contactus.html', {'form': form})





from django.shortcuts import render, get_object_or_404
from .models import Employee
@login_required
#@user_passes_test(superuser_required, login_url='welcome')  # Redirect non-superusers to welcome page
def employee_detail(request, username):
    # Fetch the Employee using the username (the user is linked to the Employee model)
    employee = get_object_or_404(Employee, user__username=username)   
    return render(request, 'employee_detail.html', {'employee': employee})



