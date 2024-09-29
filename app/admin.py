from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from import_export.admin import ImportExportMixin
from rangefilter.filters import DateRangeFilter
from import_export import resources 


class PersonResource(resources.ModelResource):
    class Meta:
        model = Person
        fields = ('check_number', 'image', 'simu', 'status')  # Excluded 'registered_date'
        import_id_fields = ('check_number',)
@admin.register(Person)
class PersonAdmin(ImportExportModelAdmin):
    resource_class = PersonResource
    list_display = ('check_number','image', 'simu', 'registered_date')
    list_filter = ('registered_date', ('registered_date', DateRangeFilter))
    search_fields = ('check_number', 'simu',)
    readonly_fields = ('registered_date',)
    list_per_page = 8
    list_max_show_all = 8
    
@admin.register(PersonReset)
class PersonAdminReset(ImportExportModelAdmin):
    list_display = ('check_number','image', 'simu', 'registered_date')
    list_filter = ('registered_date', ('registered_date', DateRangeFilter))
    search_fields = ('check_number', 'simu',)
    readonly_fields = ('registered_date',)
    list_per_page = 8
    list_max_show_all = 8

    def full_name_display(self, obj):
        return obj.full_name()
    full_name_display.short_description = 'Full Name'

class PayrollResource(resources.ModelResource):
    class Meta:
        model = Payroll
        fields = ('department', 'checkNumber', 'department', 'fname', 'mname', 'lname', 'bankName', 'accountNumber', 'grossAmount', 'basicSalary', 'netAmount', 'netAmount', 'allowance',)
        import_id_fields = ['checkNumber']  # Specify the field used as import identifier PK

    def before_import_row(self, row, **kwargs):
        row.pop('id', None)  # Exclude 'id' field from import
        for key in row:
            value = row[key]
            if isinstance(value, str):
                row[key] = value.lower().capitalize()
                
                
@admin.register(Payroll)
class PayrollAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class =PayrollResource
    readonly_fields = [field.name for field in Payroll._meta.get_fields()]
    list_display = [field.name for field in Payroll._meta.get_fields()]
    list_per_page = 5 
    list_max_show_all = 5
    ordering = ['-created_at']
    date_hierarchy = 'created_at' 
    search_fields = ('department', 'checkNumber', 'fname', 'mname', 'lname', 'bankName',) 
    actions = ['delete_all', 'delete_selected']
    def get_actions(self, request):
        # Get all actions
        actions = super().get_actions(request)
        
        # Remove delete actions if the user is not a superuser
        if not request.user.is_superuser:
            if 'delete_all' in actions:
                del actions['delete_all']
            if 'delete_selected' in actions:
                del actions['delete_selected']
                
        return actions

    def has_delete_permission(self, request, obj=None):
        # Allow delete permission only for superusers
        return request.user.is_superuser

    def delete_all(self, request, queryset):
        # Delete all objects in the Payroll model
        Payroll.objects.all().delete()
        self.message_user(request, "All items have been deleted.")
    delete_all.short_description = "Delete all items"

 
