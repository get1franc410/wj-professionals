# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\core\fixtures\company_data.py
"""
Company Information Data
========================
Initial data for Company model
"""

COMPANY_DATA = {
    'name': 'WJ Professionals',
    'tagline': 'Your Trusted Accounting Partner in Nigeria',
    'description': '''
    <p>WJ Professionals is a leading accounting and financial services firm based in Nigeria, 
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
    <p>Founded in 2010, WJ Professionals began as a small accounting practice with a big vision: 
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
    
    # Contact Information
    'email': 'info@wjprofessionals.com',
    'phone': '+234-803-065-5969',
    'address': '''Plot 123, Ademola Adetokunbo Crescent,
Wuse II, Abuja, FCT
Nigeria''',
    'city': 'Abuja',
    'state': 'FCT',
    'postal_code': '900001',
    'country': 'Nigeria',
    
    # Online Presence
    'website': 'https://www.wjprofessionals.com',
    'linkedin': 'https://linkedin.com/company/wj-professionals',
    'twitter': 'https://twitter.com/wjprofessionals',
    'facebook': 'https://facebook.com/wjprofessionals',
    'instagram': 'https://instagram.com/wjprofessionals',
    
    # Business Stats - THESE ARE THE KEY ONES FOR YOUR TEMPLATES
    'established_year': 2010,  # This calculates years_of_experience automatically
    'clients_served': 500,    # This shows in your stats
    'projects_completed': 1200, # This shows in your stats
    
    'working_hours': '''
        Monday - Friday: 8:00 AM - 6:00 PM
        Saturday: 9:00 AM - 2:00 PM
        Sunday: Closed

        Emergency Support: Available 24/7 for urgent matters
        ''',
    'certifications': [
        'Institute of Chartered Accountants of Nigeria (ICAN)',
        'Association of National Accountants of Nigeria (ANAN)',
        'Chartered Institute of Taxation of Nigeria (CITN)',
        'ISO 9001:2015 Quality Management System'
    ],
    
    # Legacy fields for backward compatibility
    'email_primary': 'info@wjprofessionals.com',
    'email_secondary': 'admin@wjprofessionals.com',
    'phone_primary': '+234-803-065-5969',
    'phone_secondary': '+234-701-987-6543',

    'rating_breakdown': {
        5: 18,  # 18 five-star reviews (75%)
        4: 6,   # 6 four-star reviews (25%)  
        3: 1,   # 1 three-star review (4%)
        2: 0,   # 0 two-star reviews
        1: 0,   # 0 one-star reviews
    },
    'total_reviews': 25,  
    'overall_rating': 4.7,  
    'rating_sources': [
        {'name': 'Google Reviews', 'rating': 4.8, 'count': 25},
        {'name': 'Facebook', 'rating': 4.6, 'count': 15},
        {'name': 'LinkedIn', 'rating': 4.7, 'count': 8},
    ],
    'featured_reviews': [
    # 5-Star Reviews (Excellent Service)
    {
        'rating': 5,
        'text': 'Exceptional service! WJ Professionals handled our company audit with utmost professionalism. Their attention to detail and thorough approach gave us complete confidence in our financial reporting.',
        'author': 'Sarah Johnson',
        'company': 'Tech Solutions Ltd',
        'date': '2024-05-15'
    },
    {
        'rating': 5,
        'text': 'Their tax advisory services saved us significant money. Highly recommended! The team identified deductions we never knew existed and helped us stay compliant with FIRS regulations.',
        'author': 'Michael Adebayo',
        'company': 'Adebayo Enterprises',
        'date': '2024-04-22'
    },
    {
        'rating': 5,
        'text': 'WJ Professionals transformed our chaotic bookkeeping into a streamlined system. Their monthly financial reports are clear, accurate, and delivered on time. Best decision we made for our business!',
        'author': 'Funmi Okafor',
        'company': 'Okafor Fashion House',
        'date': '2024-05-08'
    },
    {
        'rating': 5,
        'text': 'Outstanding VAT compliance support! They helped us navigate the complex VAT registration process and set up automated systems. No more sleepless nights during tax season.',
        'author': 'Dr. Ibrahim Musa',
        'company': 'Musa Medical Center',
        'date': '2024-04-30'
    },
    {
        'rating': 5,
        'text': 'Professional, reliable, and incredibly knowledgeable. WJ Professionals handled our IPO financial preparation flawlessly. Their expertise in Nigerian corporate law is unmatched.',
        'author': 'Jennifer Okwu',
        'company': 'Okwu Industries Plc',
        'date': '2024-03-18'
    },
    {
        'rating': 5,
        'text': 'Excellent payroll management services! They handle everything from PAYE calculations to pension contributions. Our HR team can now focus on strategic initiatives instead of number crunching.',
        'author': 'Emeka Nwosu',
        'company': 'Nwosu Construction Ltd',
        'date': '2024-05-02'
    },
    {
        'rating': 5,
        'text': 'Their business advisory services helped us secure a ₦50M loan from our bank. The financial projections and business plan they prepared were comprehensive and professional.',
        'author': 'Aisha Bello',
        'company': 'Bello Agro Ventures',
        'date': '2024-04-12'
    },
    {
        'rating': 5,
        'text': 'WJ Professionals saved our startup! Their forensic accounting services uncovered financial irregularities that could have destroyed our company. Thorough, discreet, and professional.',
        'author': 'David Ogundimu',
        'company': 'Ogundimu Tech Hub',
        'date': '2024-03-25'
    },

    # 4-Star Reviews (Very Good Service)
    {
        'rating': 4,
        'text': 'Very good service overall. The team is knowledgeable and responsive. Only minor issue was some delays during peak tax season, but they communicated well and delivered quality work.',
        'author': 'Blessing Ogbonna',
        'company': 'Ogbonna Trading Co.',
        'date': '2024-04-05'
    },
    {
        'rating': 4,
        'text': 'Solid accounting firm with good expertise in manufacturing sector. They helped streamline our cost accounting processes. Would recommend, though their fees are slightly above market rate.',
        'author': 'Chidi Anyanwu',
        'company': 'Anyanwu Manufacturing',
        'date': '2024-03-30'
    },
    {
        'rating': 4,
        'text': 'Great experience with their tax planning services. The team provided valuable insights for our expansion plans. Communication could be more frequent, but results speak for themselves.',
        'author': 'Fatima Al-Hassan',
        'company': 'Al-Hassan Logistics',
        'date': '2024-04-18'
    },
    {
        'rating': 4,
        'text': 'Professional audit services for our NGO. They understood the unique requirements of non-profit accounting and delivered a comprehensive report. Minor delays but excellent quality.',
        'author': 'Rev. Peter Adeyemi',
        'company': 'Hope Foundation Nigeria',
        'date': '2024-03-12'
    },
    {
        'rating': 4,
        'text': 'Good value for money. Their bookkeeping services are reliable and their monthly reports are detailed. The online portal for document sharing is very convenient.',
        'author': 'Isaac Adebayo',
        'company': 'Adebayo Catering Services',
        'date': '2024-04-28'
    },

    # Individual Client Reviews
    {
        'rating': 5,
        'text': 'As a freelance consultant, I needed help with personal tax planning. WJ Professionals provided excellent guidance on tax optimization strategies. Very satisfied with their individual services.',
        'author': 'Olumide Bakare',
        'company': 'Individual Client',
        'date': '2024-05-10'
    },
    {
        'rating': 5,
        'text': 'Helped me set up my small business properly from day one. From business registration to tax registration, they handled everything professionally. Great support for entrepreneurs!',
        'author': 'Tobiaz Eze',
        'company': 'Eze Beauty Salon',
        'date': '2024-04-20'
    },
    {
        'rating': 4,
        'text': 'Good experience with their personal tax filing services. They identified several deductions I missed and got me a nice refund. Will definitely use them again next year.',
        'author': 'Tunde Olatunji',
        'company': 'Individual Client',
        'date': '2024-03-28'
    },

    # Sector-Specific Reviews
    {
        'rating': 5,
        'text': 'Excellent understanding of oil & gas sector accounting. Their expertise in joint venture accounting and petroleum profit tax is outstanding. Highly recommend for energy companies.',
        'author': 'Engr. Bola Adeyinka',
        'company': 'Adeyinka Petroleum Services',
        'date': '2024-04-15'
    },
    {
        'rating': 5,
        'text': 'Perfect for hospitality businesses! They understand the unique challenges of our industry - from multiple revenue streams to seasonal fluctuations. Great sector expertise.',
        'author': 'Chief Mrs. Adunni Olashore',
        'company': 'Olashore Hotels & Resorts',
        'date': '2024-03-22'
    },
    {
        'rating': 4,
        'text': 'Good experience with their real estate accounting services. They helped us navigate the complex tax implications of our property developments. Knowledgeable team.',
        'author': 'Alhaji Musa Garba',
        'company': 'Garba Properties Ltd',
        'date': '2024-04-08'
    },

    # Technology & Innovation Reviews
    {
        'rating': 5,
        'text': 'Love their digital approach! The cloud-based accounting system they set up for us is fantastic. Real-time reporting and mobile access make business management so much easier.',
        'author': 'Chioma Okoro',
        'company': 'Okoro Digital Agency',
        'date': '2024-05-05'
    },
    {
        'rating': 4,
        'text': 'Their new accounting software is impressive. User-friendly interface and great integration with our existing systems. Still learning all features but very promising.',
        'author': 'Ahmed Lawal',
        'company': 'Lawal Import/Export',
        'date': '2024-04-25'
    },

    # Long-term Client Reviews
    {
        'rating': 5,
        'text': 'Been with WJ Professionals for 8 years now. They\'ve grown with our business from a small startup to a multi-million naira company. Consistent quality and trusted advisors.',
        'author': 'Mrs. Folake Adebisi',
        'company': 'Adebisi Group of Companies',
        'date': '2024-03-15'
    },
    {
        'rating': 5,
        'text': 'Five years of excellent service! They\'ve handled our accounting through business expansion, acquisitions, and even during COVID-19 challenges. True business partners.',
        'author': 'Engr. Kola Ogunleye',
        'company': 'Ogunleye Engineering Ltd',
        'date': '2024-04-10'
    },

    # Recent Service Expansions
    {
        'rating': 5,
        'text': 'Their new business valuation services are top-notch. Needed valuation for merger discussions and they delivered a comprehensive report that impressed all stakeholders.',
        'author': 'Dr. Amina Yusuf',
        'company': 'Yusuf Pharmaceuticals',
        'date': '2024-05-12'
    },
    {
        'rating': 4,
        'text': 'Good training workshop on the new Finance Act. The team explained complex tax changes in simple terms. Very useful for business owners trying to stay compliant.',
        'author': 'Segun Adeyemi',
        'company': 'Adeyemi Motors',
        'date': '2024-04-03'
    },

    # 3-Star Review (Good but with areas for improvement)
    {
        'rating': 3,
        'text': 'Decent service but room for improvement. The work quality is good but communication could be better. Sometimes hard to reach during busy periods. Overall satisfactory experience.',
        'author': 'Patience Okafor',
        'company': 'Okafor Ventures',
        'date': '2024-03-20'
    },
]

}

