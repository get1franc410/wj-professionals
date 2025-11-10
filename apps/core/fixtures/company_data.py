# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\core\fixtures\company_data.py
"""
Company Information Data - SINGLE SOURCE OF TRUTH
================================================
This file contains ALL company information used throughout the application.
Update this file to change company details across the entire website.
"""

COMPANY_DATA = {
    # ✅ CORE COMPANY INFO (Real Details)
    'name': 'Wole Joshua & Co.',
    'tagline': 'Your Trusted Accounting Partner in Nigeria',
    'legal_name': 'Wole Joshua & Co. (Chartered Accountants)',
    
    # ✅ REAL CONTACT INFORMATION
    'email': 'info@wolejoshuaandco.com',  # ✅ Updated to real email
    'phone': '+234-803-065-5969',
    'phone_secondary': '+234-701-987-6543',
    
    # ✅ REAL ADDRESS
    'address': 'Real Tower Centre, Ekukinam Street, Utako',  # ✅ Real address
    'city': 'Abuja',
    'state': 'FCT',
    'country': 'Nigeria',
    'full_address': 'Real Tower Centre, Ekukinam Street, Utako-Abuja, FCT Nigeria',
    
    # ✅ DEPARTMENT EMAILS (Real emails you provided)
    'email_tax': 'tax@wolejoshuaandco.com',
    'email_audit': 'audit@wolejoshuaandco.com',
    'email_contact': 'contact@wolejoshuaandco.com',
    'email_wole': 'wole@wolejoshuaandco.com',
    
    # ✅ BUSINESS DETAILS
    'established_year': 2010,
    'registration_number': 'RC-1234567',  # Update with real RC number
    'tax_id': 'TIN-12345678',  # Update with real TIN
    
    # ✅ ONLINE PRESENCE
    'website': 'https://www.wolejoshuaandco.com',
    'linkedin': 'https://linkedin.com/company/wole-joshua-co',
    'twitter': 'https://twitter.com/wolejoshuaco',
    'facebook': 'https://facebook.com/wolejoshuaco',
    'instagram': 'https://instagram.com/wolejoshuaco',
    
    # ✅ STATISTICS (Your templates use these)
    'clients_served': 500,
    'projects_completed': 1200,
    'years_experience_calculated': True,  # Auto-calculate from established_year
    
    # ✅ DESCRIPTIONS
    'description': '''
    <p>Wole Joshua & Co. is a leading accounting and financial services firm based in Nigeria, 
    providing comprehensive solutions to individuals, small businesses, and corporations across 
    the country. With over a decade of experience, we have established ourselves as a trusted 
    partner for all your financial needs.</p>
    
    <p>Our team of certified accountants, tax specialists, and financial advisors are committed 
    to delivering exceptional service while maintaining the highest standards of professionalism 
    and integrity.</p>
    ''',
    'mission': '''
    <p>To provide exceptional accounting, tax, and financial advisory services that empower our 
    clients to achieve their financial goals while ensuring full compliance with Nigerian tax 
    laws and regulations.</p>
    
    <p>We strive to build long-lasting relationships with our clients by delivering personalized 
    solutions that add real value to their businesses and personal financial management.</p>
    ''',
    'vision': '''
    <p>To be the most trusted and innovative accounting firm in Nigeria, recognized for our 
    expertise, integrity, and commitment to client success.</p>
    
    <p>We envision a future where every Nigerian business and individual has access to 
    professional financial guidance that enables them to thrive in an ever-changing economic 
    landscape.</p>
    ''',
    'values': '''
    <div class="row">
        <div class="col-md-6">
            <h4><i class="fas fa-shield-alt text-primary me-2"></i>Integrity</h4>
            <p>We maintain the highest ethical standards in all our professional dealings.</p>
        </div>
        <div class="col-md-6">
            <h4><i class="fas fa-award text-primary me-2"></i>Excellence</h4>
            <p>We strive for excellence in every service we provide to our clients.</p>
        </div>
        <div class="col-md-6">
            <h4><i class="fas fa-handshake text-primary me-2"></i>Trust</h4>
            <p>Building lasting relationships through transparency and reliability.</p>
        </div>
        <div class="col-md-6">
            <h4><i class="fas fa-lightbulb text-primary me-2"></i>Innovation</h4>
            <p>Embracing technology and modern solutions for better service delivery.</p>
        </div>
    </div>
    ''',
    'about_us': '''
    <h3>Our Story</h3>
    <p>Founded in 2010, Wole Joshua & Co. began as a small accounting practice with a big vision: 
    to provide world-class financial services to Nigerian businesses and individuals. Over the years, 
    we have grown from a two-person team to a full-service accounting firm with multiple offices 
    and a diverse client base.</p>
    
    <h3>What Sets Us Apart</h3>
    <ul>
        <li><strong>Local Expertise:</strong> Deep understanding of Nigerian tax laws and business environment</li>
        <li><strong>Technology-Driven:</strong> Modern tools and software for efficient service delivery</li>
        <li><strong>Client-Focused:</strong> Personalized attention and tailored solutions</li>
        <li><strong>Continuous Learning:</strong> Regular training to stay updated with regulatory changes</li>
    </ul>
    
    <h3>Our Commitment</h3>
    <p>We are committed to helping our clients navigate the complex world of finance and taxation 
    while focusing on their core business activities. Our success is measured by the success of 
    our clients.</p>
    ''',
    
    # ✅ WORKING HOURS
    'working_hours': '''
    Monday - Friday: 8:00 AM - 6:00 PM
    Saturday: 9:00 AM - 2:00 PM
    Sunday: Closed
    Emergency Support: Available 24/7 for urgent matters
    ''',
    
    # ✅ CERTIFICATIONS
    'certifications': [
        'Institute of Chartered Accountants of Nigeria (ICAN)',
        'Association of National Accountants of Nigeria (ANAN)',
        'Chartered Institute of Taxation of Nigeria (CITN)',
        'ISO 9001:2015 Quality Management System'
    ],
    
    # ✅ LEGACY FIELDS (for backward compatibility)
    'email_primary': 'info@wolejoshuaandco.com',
    'email_secondary': 'contact@wolejoshuaandco.com',
    'phone_primary': '+234-803-065-5969',
    'phone_secondary': '+234-701-987-6543',
}

# ✅ DEPARTMENT CONTACT INFO
DEPARTMENT_CONTACTS = {
    'tax': {
        'name': 'Tax Department',
        'email': 'tax@wolejoshuaandco.com',
        'phone': '+234-803-065-5969',
        'description': 'All tax-related services and compliance matters'
    },
    'audit': {
        'name': 'Audit Department', 
        'email': 'audit@wolejoshuaandco.com',
        'phone': '+234-803-065-5969',
        'description': 'Independent audit and assurance services'
    },
    'general': {
        'name': 'General Inquiries',
        'email': 'info@wolejoshuaandco.com',
        'phone': '+234-803-065-5969',
        'description': 'General information and initial consultations'
    },
    'contact': {
        'name': 'Contact Center',
        'email': 'contact@wolejoshuaandco.com', 
        'phone': '+234-803-065-5969',
        'description': 'Customer service and support'
    },
    'wole': {
        'name': 'Managing Partner',
        'email': 'wole@wolejoshuaandco.com',
        'phone': '+234-803-065-5969',
        'description': 'Direct contact with Managing Partner'
    }
}

# ✅ TEMPLATE DEFAULTS (Fallback values for templates)
TEMPLATE_DEFAULTS = {
    'company_name': COMPANY_DATA['name'],
    'company_email': COMPANY_DATA['email'],
    'company_phone': COMPANY_DATA['phone'],
    'company_address': COMPANY_DATA['full_address'],
    'company_tagline': COMPANY_DATA['tagline'],
}
