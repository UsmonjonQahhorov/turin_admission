from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from apps.users import serializers
from apps.users.models import Applicant, ExamDate, ExamRegistration, Program, ProgramExamdate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated




"""Aplicant Create View Test"""
class AplicantCreateView(CreateAPIView):
    serializer_class = serializers.ApplicantRegistrationSerializer
    parser_classes = MultiPartParser, FormParser

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class AplicantListView(ListAPIView):
    serializer_class = serializers.ApplicantRetriveSerializer
    queryset = Applicant.objects.all()

    def get(self, request, *args, **kwargs):
        applicants = Applicant.objects.all()
        serializer = self.serializer_class(applicants, many=True)
        return JsonResponse(serializer.data, safe=False)
    


class ApplicantRetriveView(ListAPIView):
    serializer_class = serializers.ApplicantRetriveSerializer
    queryset = Applicant.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        applicant = Applicant.objects.get(id=self.request.user.id)
        serializer = self.serializer_class(applicant)
        return JsonResponse(serializer.data, safe=False)
    

    
"""Applicant update View"""
class ApplicantUpdateView(UpdateAPIView):
    serializer_class = serializers.ApplicantUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = MultiPartParser, FormParser

    def get_object(self):
        return self.request.user
    
    def get(self, request, *args, **kwargs):
        """Return the current user's data before updating"""
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        if 'password' in serializer.validated_data:
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.validated_data["upd_status"] = True
        serializer.save()

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    

class ApplicantPassUpdateView(UpdateAPIView):
    serializer_class = serializers.ApplicantPassUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        if 'password' in serializer.validated_data:
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.validated_data["upd_status"] = True
        serializer.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)




"""Program Create View Test"""
class ProgramCreateView(CreateAPIView):
    serializer_class = serializers.ProgramSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



"""Program List View Test"""
class ProgramListView(ListAPIView):
    serializer_class = serializers.ProgramSerializer
    queryset = Program.objects.all()

    def get(self, request, *args, **kwargs):
        print(self.request.user.id)
        programs = Program.objects.all()
        serializer = self.serializer_class(programs, many=True)
        return JsonResponse(serializer.data, safe=False)
    

class ProgramUpdate(UpdateAPIView):
    serializer_class = serializers.ProgramSerializer


class ProgramDestroy(DestroyAPIView):
    serializer_class = serializers.ProgramSerializer



    

"""PROGRAM CRUD CLOSED"""


"""Exam Registration Create View Test"""
class ExamRegistrationCreateView(CreateAPIView):
    serializer_class = serializers.ExamRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

"""Exam Registration List View Test"""
class ExamRegistrationListView(ListAPIView):
    serializer_class = serializers.RegistrationRetriveSerialize
    permission_classes = [IsAuthenticated]  # ✅ Require authentication

    def get_queryset(self):
        return ExamRegistration.objects.filter(aplicant=self.request.user)
    

class ExamRegisterUpdate(UpdateAPIView):
    serializer_class=serializers.RegisterUpdateSer
    
"""EXAM REGISTRATION CRUD CLOSED"""


    


"""Exam Dates Views"""

class ExamDatesListView(ListAPIView):
    serializer_class = serializers.ExamDateSerializer
    queryset = ExamDate.objects.all()

    def get(self, request, *args, **kwargs):
        exam_dates = ExamDate.objects.all()
        serializer = self.serializer_class(exam_dates, many=True)
        return JsonResponse(serializer.data, safe=False)
    

from rest_framework.views import APIView



class ExamDateDeleteView(DestroyAPIView):
    serializer_class = serializers.ExamDateUpdate


class ExamDatePost(CreateAPIView):
    serializer_class = serializers.ExamDateSerializer



class ExamDateProgram(ListAPIView):
    serializer_class = serializers.ProgramExamDateSer
    queryset = ProgramExamdate.objects.all()


"""EXAM DATE CRUD CLOSED"""



