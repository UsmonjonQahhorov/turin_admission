import re
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from apps.users.choices import Status
from .models import Applicant, ExamDate, ExamRegion, ExamRegistration, Program, ExamAttempt
from django.contrib.auth.hashers import make_password

        


class ApplicantRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = [
            'first_name',
            'last_name',
            'email',
            'birthdate',
            'phone_number',
            'password',
            'institution',
            'language_certificates',
            'gender',
            'program',
            'file',
            'image',

        ]
    
    def validate_phone_number(self, value):
        if not value:
            raise serializers.ValidationError("Telefon raqamni kiritishingiz majburiy!")
        if Applicant.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Ushbu telefon raqam allaqachon ro'yxatdan o'tgan.")
        return value
    
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])  # ✅ Hash the password
        return super().create(validated_data)
    
class ApplicantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        exclude = ["created_at", "updated_at", "last_login", "is_staff", "is_superuser", "password", 'groups', 'user_permissions']



class ApplicantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        exclude = ["created_at", "updated_at", "last_login", "is_staff", "is_superuser", "password", 'groups', 'user_permissions']


class ApplicantPassUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    current_password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Applicant
        fields = [
            'phone_number', 
            'current_password',
            'password',
        ]
        extra_kwargs = {
            'phone_number': {'required': False},
        }
    
    def validate(self, attrs):
        if 'password' in attrs and 'current_password' not in attrs:
            raise serializers.ValidationError({"current_password": "Current password is required to set a new password"})
            
        if 'current_password' in attrs and 'password' in attrs:
            if not self.instance.check_password(attrs['current_password']):
                raise serializers.ValidationError({"current_password": "Current password is incorrect"})
            
        if 'current_password' in attrs:
            attrs.pop('current_password')
            
        return attrs
    
    def validate_phone_number(self, value):
        if value and Applicant.objects.filter(phone_number=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = "__all__"


"""Exam Registration Serializer"""
class ExamRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamRegistration
        exclude = ['status', 'aplicant']    

    def create(self, validated_data):
        user = self.context["request"].user
        program = validated_data['program']
        exam_date = validated_data['exam_date']

        exam_registration, created = ExamRegistration.objects.get_or_create(
            aplicant=user,
            program=program,
            defaults={'exam_date': exam_date, 'status': Status.PENDING_PAYMENT}
        )

        last_attempt = ExamAttempt.objects.filter(registration=exam_registration).order_by('-attempt_number').first()
        next_attempt_number = (last_attempt.attempt_number + 1) if last_attempt else 1

        ExamAttempt.objects.create(
            registration=exam_registration,
            attempt_number=next_attempt_number
        )

        return exam_registration
    

class ExamAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamAttempt
        exclude = ['registration']



class ExamRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamRegion
        fields = "__all__"


class ExamDateSerializer(serializers.ModelSerializer):
    region = ExamRegionSerializer()

    class Meta:
        model = ExamDate
        fields = "region", "date"


class AplicantRetriveExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ["first_name", "last_name"]
    

class RegistrationRetriveSerialize(serializers.ModelSerializer):
    program = ProgramSerializer()
    # result = ExamAttemptSerializer()
    aplicant = AplicantRetriveExamSerializer()
    exam_date = ExamDateSerializer()
    class Meta:
        model = ExamRegistration
        fields = ["aplicant", "exam_date", "status", "program"]
        
  
    





    
    """Login Serializer"""
class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    # def validate(self, data):
    #     user = authenticate(username=data["username"], password=data["password"])
    #     if not user:
    #         raise serializers.ValidationError(_("Invalid username or password"))
    #     return {"user": user}
    


class ApplicantRetriveSerializer(serializers.ModelSerializer):
    program = ProgramSerializer()
    class Meta:
        model = Applicant
        fields = [
        'first_name',
        'last_name',
        'email',
        'birthdate',
        'phone_number',
        'institution',
        "language_certificates",
        "gender",
        "file",
        "image",
        "program",
        ]