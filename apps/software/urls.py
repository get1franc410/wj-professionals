# apps/software/urls.py
from django.urls import path
from . import views

app_name = 'software'

urlpatterns = [
    path('accounting-software/', views.accounting_software, name='accounting_software'),
    path('purchase/', views.purchase_form, name='purchase_form'),
    path('process-purchase/', views.process_purchase, name='process_purchase'),
]
