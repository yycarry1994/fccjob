from django.contrib import admin
from jobs.models import Job

# Register your models here.


class JobAdmin(admin.ModelAdmin):
    exclude = ('creator', 'create_date', 'update_date')
    list_display = ('job_name', 'job_type', 'job_city', 'creator', 'create_date', 'update_date')

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Job, JobAdmin)