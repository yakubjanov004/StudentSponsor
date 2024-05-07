from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Sponsor(BaseModel):
    class SponsorChoice(models.TextChoices):
        YURIDIK = 'yuridik', 'Yuridik shaxs'
        JISMONIY = 'jismoniy', 'Jismoniy shaxs'
    class StatusChoice(models.TextChoices):
        YANGI = 'yangi', 'Yangi'
        MODERATSIYA = 'moderatsiya', 'Moderatsiya' 
        TASDIQLANGAN = 'tasdiqlangan', 'Tasdiqlangan'
        BEKORQILINGAN = 'bekor_qilingan', 'Bekor qilingan'
    class PaymentChoice(models.TextChoices):
        CARD = 'Karta', 'Plastik karta'
        CASH = 'Naqd', 'Naqd'
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8,decimal_places=2)
    organization = models.CharField(max_length=100)
    sponsor_type = models.CharField(max_length=100, choices=SponsorChoice.choices)
    status = models.CharField(max_length=50,choices=StatusChoice)
    payment_type = models.CharField(max_length=50, choices=PaymentChoice.choices)
    
    def __str__(self):
        return self.full_name

class University(BaseModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Student(BaseModel):

    class choices(models.TextChoices):
        BAKALAVR = 'bakalavr', 'Bakalavr'
        MAGISTR = 'magistr', 'Magistr'

    full_name = models.CharField(max_length=100)
    student_type = models.CharField(max_length=100, choices=choices)
    phone = models.CharField(max_length=100)
    university = models.ForeignKey(University,on_delete=models.PROTECT)
    contract = models.DecimalField(max_digits=8,decimal_places=2)

    def __str__(self):
        return self.full_name

class Student_Sponsor(BaseModel):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.PROTECT, related_name='student_sponsors')
    amount = models.DecimalField(max_digits=8,decimal_places=2)
    student = models.ForeignKey(Student,on_delete=models.PROTECT, related_name='student_sponsors')

   
