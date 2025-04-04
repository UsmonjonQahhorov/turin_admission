import re
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from apps.users.choices import Status
from .models import Applicant, ExamDate, ExamRegion, ExamRegistration, Program, ProgramExamdate
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
            'score',
            'file',
            'image',
            'certificates',
            'exam_date'
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
    

    def validate(self, data):
        program = data.get('program')
        exam_date = data.get('exam_date')

        if program and exam_date:
            # Check if the exam date is related to the selected program
            if not ExamDate.objects.filter(id=exam_date.id, program=program).exists():
                raise serializers.ValidationError({
                    "exam_date": f"The selected program '{program.name}' does not have an exam on {exam_date.date}. Please choose a valid exam date."
                })

        return data
    
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
        exclude = ['status', 'aplicant', "result", "ball"] 
    
    def create(self, validated_data):
        print(f"ExamRegister: {validated_data}")
        user = self.context["request"].user
        program = validated_data['program']
        exam_date = validated_data['exam_date']

        exam_registration = ExamRegistration.objects.get_or_create(
            aplicant=user,
            program=program,
            defaults={
                'exam_date': exam_date, 
                'status': Status.PENDING_PAYMENT,
                'result': None,
                'ball': None
            }
        )
        
        return exam_registration
    

    def validate(self, data):
        program = data.get('program')
        exam_date = data.get('exam_date')

        if exam_date and program and not ExamDate.objects.filter(id=exam_date.id, program=program).exists():
            raise serializers.ValidationError({
                "exam_date": f"The selected program '{program.name}' does not have an exam on {exam_date.date}. Please choose a valid exam date."
            })

        return data
    
class ExamRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamRegion
        fields = "__all__"

"""Exam Date Serializers"""
class ExamDateSerializer(serializers.ModelSerializer):
    region = ExamRegionSerializer()

    class Meta:
        model = ExamDate
        fields = "region", "date"


class ExamDateUpdate(serializers.ModelField):
    class Meta:
        fields = "__all__"


class AplicantRetriveExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ["first_name", "last_name"]
    

class RegistrationRetriveSerialize(serializers.ModelSerializer):
    program = ProgramSerializer()
    aplicant = AplicantRetriveExamSerializer()
    exam_date = ExamDateSerializer()

    class Meta:
        model = ExamRegistration
        fields = ["aplicant", "exam_date", "status", "program", "result", "ball"]
        
  
class RegisterUpdateSer(serializers.ModelSerializer):
    class Meta:
        model = ExamRegistration
        fields = ["program", "exam_date"]
    
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
    exam_date = ExamDateSerializer()
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
        "exam_date",
        'score',
        ]



"""Exam dates"""

class ProgramExamDateSer(serializers.ModelSerializer):
    programs = ProgramSerializer()
    exam_dates = ExamDateSerializer()
    class Meta:
        model = ProgramExamdate
        fields = ["programs", "exam_dates"]