from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


#----------------------------------Branch--------------------------------------
class Branch(models.Model):
    name = models.CharField(max_length=100, verbose_name="Branch Name", unique=True)
    registered_date_auto = models.DateTimeField(auto_now_add=True, verbose_name="Registered Date")

     #convert name to lower case
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.full_clean()  # Call full_clean to run the clean method
        super(Branch, self).save(*args, **kwargs)

    def clean(self):
        # Check for unique constraint on the lowercase name
        if Branch.objects.filter(name__iexact=self.name).exists():
            raise ValidationError(f"The name '{self.name}' already exists.")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branch"

class District(models.Model):
    name = models.CharField(max_length=100, verbose_name="District Name",unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name="Branch")
    registered_date_auto = models.DateTimeField(auto_now_add=True, verbose_name="Registered Date",unique=True)

    #convert name to lower case
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(District, self).save(*args, **kwargs)
    class Meta:
        verbose_name = "District"
        verbose_name_plural = "District"

    #validate if duplicate names
    def clean(self):
        # Check for unique constraint on the lowercase name
        if District.objects.filter(name__iexact=self.name).exists():
            raise ValidationError(f"The name '{self.name}' already exists.")

    def __str__(self):
        return self.name
#----------------------------------post--------------------------------------
class Post(models.Model):
    name = models.CharField(max_length=100, verbose_name="Post Name", unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name="Branch")
    registered_date_auto = models.DateTimeField(auto_now_add=True, verbose_name="Registered Date")

     #convert name to lower case
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.full_clean()  # Call full_clean to run the clean method
        super(Post, self).save(*args, **kwargs)

    def clean(self):
        # Check for unique constraint on the lowercase name
        if Post.objects.filter(name__iexact=self.name).exists():
            raise ValidationError(f"The name '{self.name}' already exists.")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Post"

#----------------------------------Role--------------------------------------
class Role(models.Model):
    role = models.CharField(max_length=50, verbose_name="Employee Role", unique=True)
    registered_date_auto = models.DateTimeField(auto_now_add=True, verbose_name="Registered Date")

    #convert name to lower case
    def save(self, *args, **kwargs):
        self.role = self.role.lower()
        self.full_clean()  # Call full_clean to run the clean method
        super(Role, self).save(*args, **kwargs)

    def clean(self):
        # Check for unique constraint on the lowercase role
        if Role.objects.filter(role__iexact=self.role).exists():
            raise ValidationError(f"The role '{self.role}' already exists.")

    def __str__(self):
        return self.role

#----------------------------------Payroll--------------------------------------
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

#----------------------------------AbstractEmployee--------------------------------------
class AbstractEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="user_role",)
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name="Registered Date")
    force_number = models.CharField(max_length=12, null=True, blank=True, verbose_name="Force Number",)
    rank = models.CharField(max_length=10, null=True, blank=True, verbose_name="Rank",)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Post",)
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="District",)
    email = models.EmailField(null=True, blank=True,)
    phone = models.IntegerField(null=True, blank=True,)
    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.username} - {self.role}"
class Employee(AbstractEmployee):
    pass


#----------------------------------New URA MOBILE USER--------------------------------------

class Person(models.Model):
    check_number = models.CharField(max_length=20,primary_key=True,)
    image = models.FileField(upload_to='images/',verbose_name="Upload Ura mobile form")  # Changed email to ImageField
    simu = models.CharField(max_length=10, unique=True, verbose_name="Phone number")
    registered_date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)  # New field
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def full_name(self):
        return self.check_number
    def __str__(self):
        return f"Added by {self.user} on {self.registered_date}"

    class Meta:
        verbose_name = "New Mobile Users"
        verbose_name_plural = "New Mobile Users"
        
    def save(self, *args, **kwargs):
        if not self.user:  # Ensure user is set
            from django.conf import settings
            self.user = getattr(settings, 'CURRENT_USER', None)  # Use a global variable for the user
        super(Person, self).save(*args, **kwargs)
        
#----------------------------------PIN RESET--------------------------------------
     
class PersonReset(models.Model):
    check_number = models.CharField(max_length=20)
    image = models.FileField(upload_to='images/',verbose_name="Upload Ura mobile form")  # Changed email to ImageField
    simu = models.CharField(max_length=10, unique=True, verbose_name="Old / New Phone number",null=True,blank=True)
    registered_date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)  # New field
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def full_name(self):
        return self.check_number
    
    def __str__(self):
        return f"Added by {self.user} on {self.registered_date}"

    class Meta:
        verbose_name = "Pin Reset Users"
        verbose_name_plural = "Pin Reset Users"
        
    def save(self, *args, **kwargs):    
        if not self.user:  # Ensure user is set
            from django.conf import settings
            self.user = getattr(settings, 'CURRENT_USER', None)  # Use a global variable for the user
        super(PersonReset, self).save(*args, **kwargs)
        
class MessageLog(models.Model):
    phone_number = models.CharField(max_length=10)
    #message = RichTextField()
    message = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    registered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.phone_number} - {self.message[:20]}'


