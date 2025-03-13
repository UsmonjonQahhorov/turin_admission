from django.contrib import admin
from apps.users.models import Applicant, ExamAttempt, ExamDate, ExamRegion, ExamRegistration, Program

# @admin.register(ClickOrder)
# class ClickOrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'amount']
#     list_display_links = ['id', 'amount']

#     save_on_top = True  


@admin.register(Applicant)
class AplicantAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
         'last_name',
         'birthdate',
         'phone_number',
         'email',
         'institution',
         'language_certificates',
         'gender',
         'program',
        ]
    save_on_top = True

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'exam_date']
    list_display_links = ['name', 'level', 'exam_date']

    save_on_top = True


@admin.register(ExamRegion)
class ExamRegionAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']


@admin.register(ExamDate)
class ExamDateAdmin(admin.ModelAdmin):
    list_display = ['region', 'date']
    list_display_links = ['region', 'date']

@admin.register(ExamRegistration)
class ExamRegistrationAdmin(admin.ModelAdmin):
    list_display = ['aplicant', 'program', 'exam_date', 'status', 'created_at', 'updated_at']
    list_display_links = ['aplicant', 'program', 'exam_date', 'status','created_at', 'updated_at']


# @admin.register(Document)
# class DocumentAdmin(admin.ModelAdmin):
#     list_display = ['user', 'file', 'image', 'uploaded_at']
#     list_display_links = ['user', 'file']



@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ['registration', 'attempt_number', 'result', 'ball']
    list_display_links = ['registration', 'attempt_number', 'result', 'ball']

    save_on_top = True