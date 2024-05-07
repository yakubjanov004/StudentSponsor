from django.urls import path
from app1 import views 

urlpatterns = [
    path('sponsor-list/', views.SponsorListAPIView.as_view()),
    path('sponsor-create/', views.SponsorCreateAPIView.as_view()),
    path('sponsor-update/<int:pk>/', views.SponsorUpdateAPIView.as_view()),
    

    path('talaba-list/', views.TalabaListAPIView.as_view()),
    path('talaba-create/', views.TalabaCreateAPIView.as_view()),
    path('talaba-retriece-update/', views.TalabaRetrieveAPIView.as_view()),
    path('talaba-update/<int:pk>/', views.TalabaUpdateAPIView.as_view()),

    path('sponsorStudent-list/', views.SponsorStudentListAPIView.as_view()),
    path('sponsorStudent-create/', views.SponsorStudentCreateAPIView.as_view()),
    path('sponsorStudent-update/<int:pk>/', views.SponsorStudentUpdateAPIView.as_view()),


    path('amount-statictic', views.StaticticAPIView.as_view()),
    
]