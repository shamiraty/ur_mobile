from django.shortcuts import render, redirect
from .forms import PersonForm,PersonFormReset
from django.db import models
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required


#create person
def person_create_view(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('create_person')  # Redirect back to the home page or the same form page
    else:
        form = PersonForm()

    return render(request, 'home.html', {'form': form})


#create personReset
def person_create_reset_view(request):
    if request.method == 'POST':
        form = PersonFormReset(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('create_person_reset')  # Redirect back to the home page or the same form page
    else:
        form = PersonFormReset()

    return render(request, 'homereset.html', {'form': form})


from .models import Person, Payroll
from django.db.models import Count
from .models import Payroll, Person,PersonReset

@login_required
def payroll_employee_list(request):
    # Get start_date and end_date from request parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filter Payroll records based on dates or return all Payrolls if no dates provided

    payrolls = Payroll.objects.all()  # Fallback to all records if no date range is provided

    # Get check numbers from filtered Payroll records
    payroll_check_numbers = payrolls.values_list('checkNumber', flat=True)
    
    # Fetch Persons with check_number in payroll_check_numbers
    if start_date and end_date:
     persons = Person.objects.filter(
        check_number__in=payroll_check_numbers,
        registered_date__range=[start_date, end_date]
    )
    else:
     persons = Person.objects.filter(check_number__in=payroll_check_numbers)

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
    return render(request, 'person_list.html', context)






from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Person, PersonReset

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

    # Filter Payroll records based on dates or return all Payrolls if no dates provided

    payrolls = Payroll.objects.all()  # Fallback to all records if no date range is provided

    # Get check numbers from filtered Payroll records
    payroll_check_numbers = payrolls.values_list('checkNumber', flat=True)
    
    # Fetch Persons with check_number in payroll_check_numbers
    if start_date and end_date:
     persons = PersonReset.objects.filter(
        check_number__in=payroll_check_numbers,
        registered_date__range=[start_date, end_date]
    )
    else:
     persons = PersonReset.objects.filter(check_number__in=payroll_check_numbers)

    # Create a list of dictionaries to merge both Person and Payroll data
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




def update_status_reset(request, check_number):
    if not request.user.is_authenticated:  # Check user authentication
        return HttpResponseForbidden("You are not authorized to perform this action.")
    
    person = get_object_or_404(PersonReset, id=check_number)
    
    if request.method == 'POST':
        # Toggle status
        person.status = not person.status
        person.save()
    
    return redirect('person_list_reset')  # Redirect to a view that shows the updated list


def welcome(request):
    return render(request,'welcome.html')