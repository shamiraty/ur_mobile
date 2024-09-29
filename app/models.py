from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


class Payroll(models.Model):
    department = models.CharField(verbose_name="Department", max_length=100, null=True, blank=True)
    checkNumber = models.CharField(verbose_name="Check Number", primary_key=True, max_length=100)
    fname = models.CharField(verbose_name="First Name", max_length=100, null=True, blank=True)
    mname = models.CharField(verbose_name="Middle Name", max_length=100, null=True, blank=True)
    lname = models.CharField(verbose_name="Last Name", max_length=100, null=True, blank=True)
    bankName = models.CharField(verbose_name="Bank Name", max_length=100, null=True, blank=True)
    accountNumber = models.CharField(verbose_name="Account Number", max_length=100, null=True, blank=True)
    grossAmount = models.DecimalField(verbose_name="Gross Amount", max_digits=20, decimal_places=2, null=True, blank=True)
    basicSalary = models.DecimalField(verbose_name="Basic Salary", max_digits=20, decimal_places=2, null=True, blank=True)
    netAmount = models.DecimalField(verbose_name="Net Amount", max_digits=20, decimal_places=2, null=True, blank=True)
    allowance = models.DecimalField(verbose_name="Allowance", max_digits=20, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="Created At", default=timezone.now, null=True, blank=True)

    class Meta:
        verbose_name = "Payroll"
        verbose_name_plural = "Payrolls"

    def __str__(self):
        return f"{self.fname} {self.lname}'s Payroll"


from django.db import models

class Person(models.Model):
    check_number = models.CharField(max_length=20,primary_key=True,)
    image = models.FileField(upload_to='images/',verbose_name="Upload Ura mobile form")  # Changed email to ImageField
    simu = models.CharField(max_length=10, unique=True, verbose_name="Phone number")
    registered_date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)  # New field

    def full_name(self):
        return self.check_number

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        
class PersonReset(models.Model):
    check_number = models.CharField(max_length=20)
    image = models.FileField(upload_to='images/',verbose_name="Upload Ura mobile form")  # Changed email to ImageField
    simu = models.CharField(max_length=10, unique=True, verbose_name="Old / New Phone number",null=True,blank=True)
    registered_date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)  # New field

    def full_name(self):
        return self.check_number

    class Meta:
        verbose_name = "EmployeeReset"
        verbose_name_plural = "EmployeesReset"
        
 



