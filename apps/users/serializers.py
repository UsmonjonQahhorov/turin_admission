import re
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from apps.payments.models import Payment
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





"""=========================================================Program Serializer======================================================"""
class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = "__all__"
"""=========================================================Program Serializer======================================================"""





"""Exam Registration Serializer need"""
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

    

class ExamDateSerializer(serializers.ModelSerializer): #This serializer is used to use as a subserializer, this is not main serializer. Used in several get methods
    class Meta:
        model = ExamDate
        fields = "region", "date"


"""Exam Date List Serializers"""

class ExamRegionSerializer(serializers.ModelSerializer): #This serializer is used to use as a subserializer, this is not main serializer.Used in ExamDateListSerializer
    class Meta:
        model = ExamRegion
        fields = ['name']


class ExamDateListSerializer(serializers.ModelSerializer):
    region = ExamRegionSerializer()
    class Meta:
        model = ExamDate
        fields = "id", "region", "date"



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

"""========================================================Exam Registration Model Serializer======================================================"""
        



"""========================================================Applicant Retrive Serializer======================================================"""
class ApplicantRetriveSerializer(serializers.ModelSerializer):
    program = ProgramSerializer()
    exam_date = ExamDateSerializer()
    payment_status = serializers.SerializerMethodField()
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
        "payment_status"
        ]

    def get_payment_status(self, obj):
        # Retrieve the latest payment for the applicant
        latest_payment = Payment.objects.filter(applicant=obj).order_by('-id').first()
        
        if latest_payment:
            return {
                'status': latest_payment.status,
                'amount': latest_payment.amount,
                'payment_type': latest_payment.payment_type,
                'transaction_id': latest_payment.transaction_id
            }
        return None
    
"""========================================================Applicant Retrive Serializer========================================================================="""



"""Exam dates"""
class ProgramExamDateSer(serializers.ModelSerializer):
    programs = ProgramSerializer()
    exam_dates = ExamDateSerializer()
    class Meta:
        model = ProgramExamdate
        fields = ["id","programs", "exam_dates"]


class ProgramExamUpdateDateSer(serializers.ModelSerializer):# Thi serializer is used only in UpdateAttachedExam
    programs = ProgramSerializer()
    exam_dates = ExamDateSerializer()

    class Meta:
        model = ProgramExamdate
        fields = ["id", "programs", "exam_dates"]

    def update(self, instance, validated_data):
        # Extract nested exam_dates data
        exam_dates_data = validated_data.pop("exam_dates", {})
        program_data = validated_data.pop("programs", {})

        # Update exam date
        if exam_dates_data:
            instance.exam_dates.date = exam_dates_data.get("date", instance.exam_dates.date)

            # Update region safely
            if "region" in exam_dates_data and isinstance(exam_dates_data["region"], dict):
                instance.exam_dates.region.name = exam_dates_data["region"].get("name", instance.exam_dates.region.name)
                instance.exam_dates.region.save()

            instance.exam_dates.save()

        # Update program safely
        if program_data:
            instance.programs.name = program_data.get("name", instance.programs.name)
            instance.programs.save()

        instance.save()
        return instance



class ExamDateCreateSerializer(serializers.Serializer):

    program = serializers.IntegerField(required=True)
    region_name = serializers.CharField(max_length=255, required=True)
    exam_date = serializers.DateTimeField(required=True)

    def create(self, validated_data):
        program_id = validated_data["program"]
        region_name = validated_data["region_name"]
        exam_date = validated_data["exam_date"]

        program_instance = Program.objects.get(id=program_id)
        region_instance = ExamRegion(
            name=region_name
        )
        region_instance.save()

        exam_date_instance = ExamDate(
            region=region_instance,
            date=exam_date
        )
        exam_date_instance.save()
        program_exam_date = ProgramExamdate(
            programs=program_instance,
            exam_dates=exam_date_instance
        )
        program_exam_date.save()
        print(program_exam_date)
        return program_exam_date


    



