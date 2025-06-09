# apps/software/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def accounting_software(request):
    """Display accounting software information and features"""
    context = {
        'page_title': 'WJ Accounting Software',
        'meta_description': 'Professional accounting software designed for Nigerian businesses. Features include invoicing, expense tracking, tax compliance, and financial reporting.',
        'software_features': [
            {
                'icon': 'fas fa-file-invoice-dollar',
                'title': 'Invoicing & Billing',
                'description': 'Create professional invoices, track payments, and manage billing cycles.'
            },
            {
                'icon': 'fas fa-chart-line',
                'title': 'Financial Reporting',
                'description': 'Generate comprehensive financial reports including P&L, Balance Sheet, and Cash Flow.'
            },
            {
                'icon': 'fas fa-receipt',
                'title': 'Expense Management',
                'description': 'Track expenses, categorize transactions, and manage vendor payments.'
            },
            {
                'icon': 'fas fa-file-invoice',
                'title': 'Tax Compliance',
                'description': 'Nigerian tax compliance features including VAT, WHT, and FIRS reporting.'
            },
            {
                'icon': 'fas fa-users',
                'title': 'Multi-User Access',
                'description': 'Role-based access control for accountants, managers, and staff.'
            },
            {
                'icon': 'fas fa-cloud',
                'title': 'Data Backup',
                'description': 'Automatic data backup and cloud synchronization options.'
            }
        ],
        'pricing_plans': [
            {
                'name': 'SINGLE',
                'display_name': 'Single User',
                'price': 150000,  # ₦150,000
                'currency': '₦',
                'period': 'one-time',
                'installations': 1,
                'features': [
                    'Complete accounting features',
                    '1 user license',
                    '1 installation',
                    '1 year free updates',
                    'Email support'
                ],
                'popular': False
            },
            {
                'name': 'MULTI',
                'display_name': 'Multi User',
                'price': 400000,  # ₦400,000
                'currency': '₦',
                'period': 'one-time',
                'installations': 5,
                'features': [
                    'All Single User features',
                    'Up to 5 users',
                    '5 installations',
                    'Multi-branch support',
                    'Priority email support',
                    'Phone support'
                ],
                'popular': True
            },
            {
                'name': 'ENTERPRISE',
                'display_name': 'Enterprise',
                'price': 1000000,  # ₦1,000,000
                'currency': '₦',
                'period': 'one-time',
                'installations': 10,
                'features': [
                    'All Multi User features',
                    'Unlimited users',
                    '10 installations',
                    'Advanced reporting',
                    'API access',
                    'Dedicated support',
                    'Custom training'
                ],
                'popular': False
            }
        ]
    }
    return render(request, 'software/accounting_software.html', context)

def purchase_form(request):
    """Display purchase form"""
    license_type = request.GET.get('license_type', 'SINGLE')
    
    pricing = {
        'SINGLE': {'price': 150000, 'name': 'Single User', 'formatted_price': '₦150,000'},
        'MULTI': {'price': 400000, 'name': 'Multi User (5 seats)', 'formatted_price': '₦400,000'},
        'ENTERPRISE': {'price': 1000000, 'name': 'Enterprise (10 seats)', 'formatted_price': '₦1,000,000'}
    }
    
    context = {
        'selected_license': license_type,
        'pricing': pricing,
        'selected_plan': pricing.get(license_type, pricing['SINGLE']),
    }
    return render(request, 'software/purchase_form.html', context)

def process_purchase(request):
    """Process the purchase (placeholder for now)"""
    if request.method == 'POST':
        # For now, just show a success message
        customer_name = request.POST.get('customer_name', '')
        license_type = request.POST.get('license_type', '')
        
        pricing = {
            'SINGLE': '₦150,000',
            'MULTI': '₦400,000',
            'ENTERPRISE': '₦1,000,000'
        }
        
        price = pricing.get(license_type, '₦150,000')
        
        messages.success(
            request, 
            f'Thank you {customer_name}! Your interest in the {license_type} license ({price}) has been recorded. '
            'Our payment system is being finalized. We will contact you shortly to complete your purchase.'
        )
        return redirect('software:accounting_software')
    
    return redirect('software:purchase_form')
