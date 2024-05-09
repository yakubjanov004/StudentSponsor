from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView,UpdateAPIView,RetrieveAPIView,RetrieveUpdateAPIView
from app1 import serializers
from app1 import models
from rest_framework.views import APIView,Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

# Create your views here.

# Sponsor uchun
class SponsorListAPIView(ListAPIView):
    serializer_class = serializers.SponsorSerializers
    queryset = models.Sponsor.objects.all()

class SponsorCreateAPIView(CreateAPIView):
    serializer_class = serializers.SponsorSerializers
    queryset = models.Sponsor.objects.all()
    

class SponsorUpdateAPIView(UpdateAPIView):
    serializer_class = serializers.SponsorSerializers
    queryset = models.Sponsor.objects.all()


# Talaba uchun
class TalabaListAPIView(ListAPIView):
    serializer_class = serializers.StudentSerializers
    queryset = models.Student.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ('student_type', 'university')
    search_fields = ('full_name',)

class TalabaCreateAPIView(CreateAPIView):
    serializer_class = serializers.StudentCreateSerializers
    queryset = models.Student.objects.all()

class TalabaRetrieveAPIView(RetrieveAPIView):
    serializer_class = serializers.StudentSerializers
    queryset = models.Student.objects.all()
    

class TalabaUpdateAPIView(UpdateAPIView):
    serializer_class = serializers.StudentUpdateSerializers
    queryset = models.Student.objects.all()


# SponsorStudent uchun
class SponsorStudentListAPIView(ListAPIView):
    serializer_class = serializers.StudentSponsorSerializers
    queryset = models.Student_Sponsor.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ('sponsor', 'student')
    search_fields = ('sponsor', 'student',)

class SponsorStudentCreateAPIView(CreateAPIView):
    serializer_class = serializers.StudentSponsorSerializers
    queryset = models.Student_Sponsor.objects.all()


class SponsorStudentUpdateAPIView(UpdateAPIView):
    serializer_class = serializers.StudentSponsorSerializers
    queryset = models.Student_Sponsor.objects.all()

class SponsorStudentRetriveAPIView(RetrieveAPIView):
    serializer_class = serializers.StudentSponsorSerializers
    queryset = models.Student_Sponsor.objects.all()


# Qo'shimcha
class StaticticAPIView(APIView):

    def get(self, request):
        from django.db.models import Sum
        total_paid_amount = models.Student_Sponsor.objects.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        total_required_amount = models.Student.objects.aggregate(total_amount=Sum('contract'))['total_amount'] or 0
        total_unpaid_amount = total_required_amount - total_paid_amount
        return Response(
            data={
                'total_paid_amount' : total_paid_amount,
                'total_required_amount' : total_required_amount,
                'total_unpaid_amount' : total_unpaid_amount
            }
        )
    
class GraphicAPIView(APIView):

    def get(self, request):
        from datetime import datetime
        this_year = datetime.now().year
        from django.db.models import Sum
        result = []

        for i in range(1,13):
            sponsor_amount = models.Sponsor.objects.filter(
                created_at__month=i,
                created_at__year=this_year,
                status='tasdiqlangan'
            ).aggregate(total=Sum('amount'))['total'] or 0

            student_amount = models.Student.objects.filter(
                created_at__month=i,
                created_at__year=this_year,
            ).aggregate(total=Sum('contract'))['total'] or 0

            result.append({
                "month":i,
                "sponsor_amount":sponsor_amount,
                "student_amount":student_amount
            })

        return Response(result)
        
class GraphicListView(ListAPIView):
    serializer_class = serializers.GraphicSerializer

    def get_queryset(self):
        from datetime import datetime
        from django.db.models import Sum
        this_year = datetime.now().year
        queryset = []

        for i in range(1, 13):
            sponsor_amount = models.Sponsor.objects.filter(
                created_at__month=i,
                created_at__year=this_year,
                status='tasdiqlangan'
            ).aggregate(total=Sum('amount'))['total'] or 0

            student_amount = models.Student.objects.filter(
                created_at__month=i,
                created_at__year=this_year,
            ).aggregate(total=Sum('contract'))['total'] or 0

            queryset.append({
                "month": i,
                "sponsor_amount": sponsor_amount,
                "student_amount": student_amount
            })

        return queryset
    
class StaticticListView(ListAPIView):
    serializer_class = serializers.StaticticSerializer

    def get_queryset(self):
        from django.db.models import Sum
        total_paid_amount = models.Student_Sponsor.objects.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        total_required_amount = models.Student.objects.aggregate(total_amount=Sum('contract'))['total_amount'] or 0
        total_unpaid_amount = total_required_amount - total_paid_amount
        return [{
            'total_paid_amount': total_paid_amount,
            'total_required_amount': total_required_amount,
            'total_unpaid_amount': total_unpaid_amount
        }]