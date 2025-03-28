from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from apps.users import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
    path('program/', views.ProgramCreateView.as_view(), name="program-create"),
    path('program/list/', views.ProgramListView.as_view(), name="program-list"),
    path("program/update/<int:pk>", views.ProgramUpdate.as_view(), name = "program_update"),
    path("program/destroy/<int:pk>", views.ProgramDestroy.as_view(), name = "program_destroy"),


    path('applicant/', views.AplicantCreateView.as_view(), name="aplicant-create"),
    path('applicant/list/', views.AplicantListView.as_view(), name="aplicant-list"),
    path('applicant/get-me/', views.ApplicantRetriveView.as_view(), name="aplicant-retrive"),
    path('applicant/get_id/<int:pk>/', views.ApplicantRetriveView.as_view(), name='get_user_id'),
    path('applicant/update/<int:pk>', views.ApplicantUpdateView.as_view(), name="aplicant-update"),
    path('applicant/password/change/', views.ApplicantPassUpdateView.as_view(), name="change-password"),

    path('exam/registration/', views.ExamRegistrationCreateView.as_view(), name="exam-registration-create"),
    path("exam/register/update/<int:pk>", views.ExamRegisterUpdate.as_view(), name="register_update"),

    path('exam/dates/', views.ExamDatesListView.as_view(), name="exam-date-create"),
    path("exam/reg/status/", views.ExamRegistrationListView.as_view(), name="exam-registration-list"),
    path("exam/delete/<int:pk>", views.ExamDateDeleteView.as_view(), name="exam_delete"),

    path("exam/date/create/", views.ExamDatePost.as_view(), name="exam-date-create"),
    path("exam/region/create/", views.ExamRegionCreateView.as_view(), name="exam-region-create"),

    path("programs/exam/dates", views.ExamDateProgram.as_view(), name="program_exam_dates"),
    path("exam/date/attach/", views.ExamDateCreateView.as_view(), name="exam-date-attach"),

]


