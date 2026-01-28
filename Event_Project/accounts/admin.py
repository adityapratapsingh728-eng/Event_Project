from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import UserMember, CollegeData

admin.site.register(UserMember)

@admin.register(CollegeData)
class CollegeDataAdmin(ImportExportModelAdmin):
    list_display = ('college_id', 'name', 'u_role')
