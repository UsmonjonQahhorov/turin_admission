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

    path('applicant/', views.AplicantCreateView.as_view(), name="aplicant-create"),
    path('applicant/list/', views.AplicantListView.as_view(), name="aplicant-list"),
    path('applicant/get-me/', views.ApplicantRetriveView.as_view(), name="aplicant-retrive"),
    path('applicant/update/', views.ApplicantUpdateView.as_view(), name="aplicant-update"),
    path('applicant/password/change/', views.ApplicantPassUpdateView.as_view(), name="change-password"),

    path('exam/registration/', views.ExamRegistrationCreateView.as_view(), name="exam-registration-create"),
    path('exam/dates/', views.ExamDatesListView.as_view(), name="exam-date-create"),
    path("exam/reg/status/", views.ExamRegistrationListView.as_view(), name="exam-registration-list")
]
