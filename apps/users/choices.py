from django.db import models


class Nationality(models.TextChoices):
    UZBEK = ('uzbekistan', 'UZBEKISTAN')
    INTERNATIONAL = ('international', 'INTERNATIONAL')



class LanguageSertification(models.TextChoices):
    IELTS = ('ielts', 'IELTS')
    TOEFL = ('toefl', 'TOEFL')
    SAT = ('sat', 'SAT')


class DagreeProgram(models.TextChoices):
    BACHELOR = ("BACHELOR'S DAGREE", "bachelor's dagree")
    MASTER = ("MASTER'S DAGREE", "master's dagree")


# class FacultyChoices(models.TextChoices):
#     ME = ('MECHANICAL ENGINEERING','Mechanical Engineering(🇮🇹)')
#     CS = ('COMPUTER ENGINEERING','Computer Engineering(🇮🇹)')
#     CIE = ('CIVIL ENGINEERING','Civil Engineering(🇮🇹)')
#     SE = ('SOFTWARE ENGINEERING','Software Engineering')
#     AD = ('ARCHITECTURE AND DESIGN', 'Architecture and Design')
#     BM = ('BUISNESS MANAGEMENT','Business Management')
#     AE = ('AUTOMATIVE ENGINEERING', 'Automative Engineering')
#     AV = ('AVIATION ENGINEERING')
    

class GenderChoices(models.TextChoices):
    MALE = ('MALE', 'Male')
    FEMALE = ('FEMALE', "Female") 



class Status(models.TextChoices):
        PENDING_PAYMENT = "pending", "Ожидание платежа"
        CONFIRMED = "confirmed", "Оплачено"
        FAILED = "failed", "Провален"
        CANCELED = "canceled", "Отменено"



class PaymentType(models.TextChoices):
        FIRST = "first", "Первичная регистрация"
        SECOND = "second", "Вторая попытка"
        THIRD_PLUS = "third_plus", "Третья и более"


class RoleChoices(models.TextChoices):
     APLICANT = 'aplicant', 'Aplicant'
     ADMIN = 'admin', 'Admin'







    
