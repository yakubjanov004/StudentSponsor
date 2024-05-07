from dataclasses import fields

# from pyexpat import model

from rest_framework import serializers
from app1 import models


class SponsorSerializers(serializers.ModelSerializer):
    university = serializers.StringRelatedField(source='university.title')
    class Meta:
        model = models.Sponsor
        exclude = ('organization', 'sponsor_type', 'updated_at', 'payment_type',)


class StudentSponsorListSerializer(serializers.ManyRelatedField):

    class Meta:
        model = models.Student_Sponsor
        fields = ('id', 'sponsor', 'amount')
        
class StudentSerializers(serializers.ModelSerializer):
    university = serializers.StringRelatedField(source='university.title')
    from django.db.models import Sum
    allocated_amount = serializers.SerializerMethodField()
    
    def get_allocated_amount(self, obj):
        from django.db.models import Sum
        student_paid_money = obj.student_sponsors.all().aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        return student_paid_money
    
    class Meta:
        model = models.Student
        exclude = ('phone', 'created_at', 'updated_at',)
        
class StudentSponsorSerializers(serializers.ModelSerializer): 
    class Meta:
        model = models.Student_Sponsor
        fields = ('id', 'amount', 'sponsor', 'student')

        def validate(self, attrs):
            amount = attrs.get('amount')
            sponsor = attrs.get('sponsor')
            student = attrs.get('student')
            from django.db.models import Sum

            student_paid_money = student.student_sponsors.all().aggregate(total_amount=Sum('amount'))['total_amount'] or 0


            if student.contract - student_paid_money < amount:
                # raise serializers.ValidationError(detail={'error': f"Siz {student.contract - student_paid_money} pul to'lasangiz yetarli"})
                print('aaa')
                raise serializers.ValidationError(f"Yetarli mablag' mavjud emas. Siz {student.contract - student_paid_money} pul to'lasangiz yetarli")
            
            sponsor_paid_money = sponsor.student_sponsors.all().aggregate(total_amount=Sum('amount'))['total_amount'] or 0
            if sponsor.amount - sponsor_paid_money < amount:
                print('bbb')
                # raise serializers.ValidationError(
                #     detail={'error':
                #              f"Sizning xisobingizda {sponsor.amount - sponsor_paid_money} pul bor"})
                raise serializers.ValidationError(f"Xisobingizda yetarli mablag' mavjud emas. Sizning xisobingizda {sponsor.amount - sponsor_paid_money} pul bor")
            
            return attrs


class StudentSponsorRetrieveSerializer(serializers.ModelSerializer):
    sponsor = SponsorSerializers()
    student = StudentSerializers()

    class Meta:
        model = models.Student_Sponsor
        fields = ('id', 'sponsor', 'amount', 'student')




class UniversitySerializers(serializers.ModelSerializer):
    class Meta:
        model = models.University
        fields = '__all__'
        
class BaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.BaseModel
        fields = '__all__'