from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.daily_dashboard, name='daily_dashboard'),
    path('add-sale/', views.add_sale, name='add_sale'),
    path('monthly-report/', views.monthly_report, name='monthly_report'),
    path('export-excel/', views.export_excel, name='export_excel'),

]