# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\core\fixtures\staff_data.py
"""
Staff Data
==========
Initial data for Staff model
"""

STAFF_DATA = [
    {
        'first_name': 'Oluwole',  
        'last_name': 'Joshua',    
        'email': 'oluwole.joshua@wjprofessionals.com', 
        'phone': '+234-803-065-5969',
        'position': 'managing_partner',
        'department': 'management',
        'photo_path': 'images/ceo_portrait.jpg',  # Add this line for the CEO photo
        'bio': '''
        <p>Oluwole Joshua is the Managing Partner and founder of WJ Professionals. With over 15 years 
        of experience in accounting and taxation, he leads the firm's strategic direction and client 
        relationships.</p>
        
        <p>Oluwole is a Fellow of the Institute of Chartered Accountants of Nigeria (FCA) and holds 
        an MBA in Finance from the University of Lagos. He specializes in corporate taxation, audit, 
        and financial advisory services.</p>
        
        <p>Before founding WJ Professionals, Oluwole worked with PwC Nigeria for 8 years, where he 
        served various multinational clients and gained extensive experience in international taxation 
        and audit.</p>
        ''',
        'qualifications': [
            'FCA - Fellow, Institute of Chartered Accountants of Nigeria',
            'MBA Finance - University of Lagos',
            'B.Sc Accounting - Ahmadu Bello University',
            'Certified Tax Practitioner - CITN'
        ],
        'specializations': [
            'Corporate Taxation',
            'Financial Audit',
            'Business Advisory',
            'Strategic Planning',
            'International Taxation'
        ],
        'years_experience': 15,
        'is_featured': True,
        'linkedin': 'https://linkedin.com/in/oluwole-joshua',  
        'twitter': 'https://twitter.com/oluwole_joshua'       
    },
    {
        'first_name': 'Adebayo',
        'last_name': 'Ogundimu',
        'email': 'adebayo.ogundimu@wjprofessionals.com',
        'phone': '+234-809-123-4568',
        'position': 'senior_partner',
        'department': 'audit',
        'photo_path': 'images/staff_2.jpg',  # Placeholder for now
        'bio': '''
        <p>Adebayo Ogundimu is a Senior Partner specializing in audit and assurance services. 
        With 12 years of professional experience, he heads our audit department and ensures 
        the highest quality standards in all audit engagements.</p>
        
        <p>Adebayo is a Chartered Accountant (ACA) and holds a Master's degree in Business 
        Administration. He has extensive experience in statutory audits, due diligence reviews, 
        and forensic accounting.</p>
        
        <p>He has worked with various industries including manufacturing, oil & gas, banking, 
        and telecommunications, providing him with deep sector knowledge and expertise.</p>
        ''',
        'qualifications': [
            'ACA - Associate, Institute of Chartered Accountants of Nigeria',
            'MBA - University of Ibadan',
            'B.Sc Accounting - University of Ife',
            'Certified Fraud Examiner - ACFE'
        ],
        'specializations': [
            'Statutory Audits',
            'Due Diligence',
            'Forensic Accounting',
            'Risk Assessment',
            'Internal Controls'
        ],
        'years_experience': 12,
        'is_featured': True,
        'linkedin': 'https://linkedin.com/in/adebayo-ogundimu'
    },
    {
        'first_name': 'Fatima',
        'last_name': 'Abdullahi',
        'email': 'fatima.abdullahi@wjprofessionals.com',
        'phone': '+234-809-123-4569',
        'position': 'senior_manager',
        'department': 'tax',
        'photo_path': 'images/staff_3.jpg',  # Placeholder for now
        'bio': '''
        <p>Fatima Abdullahi is a Senior Tax Manager with extensive experience in Nigerian 
        taxation. She leads our tax advisory team and specializes in complex tax planning 
        and compliance issues.</p>
        
        <p>Fatima is a Chartered Tax Practitioner and holds advanced certifications in 
        international taxation. She has successfully handled tax matters for over 200 clients 
        across various industries.</p>
        
        <p>Her expertise includes VAT planning, transfer pricing, and tax dispute resolution. 
        She regularly represents clients before tax authorities and has achieved significant 
        tax savings for numerous businesses.</p>
        ''',
        'qualifications': [
            'CTP - Chartered Tax Practitioner, CITN',
            'ACA - Associate, Institute of Chartered Accountants of Nigeria',
            'M.Sc Taxation - University of Lagos',
            'B.Sc Economics - University of Abuja'
        ],
        'specializations': [
            'Corporate Tax Planning',
            'VAT Advisory',
            'Transfer Pricing',
            'Tax Dispute Resolution',
            'International Taxation'
        ],
        'years_experience': 10,
        'is_featured': True,
        'linkedin': 'https://linkedin.com/in/fatima-abdullahi'
    },
    {
        'first_name': 'Chinedu',
        'last_name': 'Okwu',
        'email': 'chinedu.okwu@wjprofessionals.com',
        'phone': '+234-809-123-4570',
        'position': 'manager',
        'department': 'accounting',
        'photo_path': 'images/staff_4.jpg',  # Placeholder for now
        'bio': '''
        <p>Chinedu Okwu is an Accounting Manager responsible for our bookkeeping and financial 
        reporting services. He ensures that all client financial records are accurate, timely, 
        and compliant with applicable standards.</p>
        
        <p>With 8 years of experience in financial accounting, Chinedu has worked with businesses 
        of all sizes, from startups to established corporations. He is proficient in various 
        accounting software and modern financial technologies.</p>
        
        <p>Chinedu holds professional certifications and is known for his attention to detail 
        and ability to streamline accounting processes for improved efficiency.</p>
        ''',
        'qualifications': [
            'ACA - Associate, Institute of Chartered Accountants of Nigeria',
            'B.Sc Accounting - University of Nigeria, Nsukka',
            'Certified QuickBooks ProAdvisor',
            'Advanced Excel Certification'
        ],
        'specializations': [
            'Financial Reporting',
            'Management Accounting',
            'Bookkeeping Systems',
            'Process Automation',
            'Financial Analysis'
        ],
        'years_experience': 8,
        'is_featured': False,
        'linkedin': 'https://linkedin.com/in/chinedu-okwu'
    },
    {
        'first_name': 'Aisha',
        'last_name': 'Mohammed',
        'email': 'aisha.mohammed@wjprofessionals.com',
        'phone': '+234-809-123-4571',
        'position': 'manager',
        'department': 'business_services',
        'photo_path': 'images/staff_5.jpg',  # Placeholder for now
        'bio': '''
        <p>Aisha Mohammed manages our business registration and compliance services. She has 
        extensive knowledge of Nigerian corporate law and regulatory requirements, helping 
        clients navigate the complex business registration landscape.</p>
        
        <p>With 7 years of experience in corporate services, Aisha has successfully registered 
        over 300 businesses and maintained ongoing compliance for numerous clients. She stays 
        current with regulatory changes and ensures clients remain compliant.</p>
        
        <p>Aisha is known for her efficiency in handling CAC processes and her ability to 
        explain complex regulatory requirements in simple terms to clients.</p>
        ''',
        'qualifications': [
            'LLB - University of Abuja',
            'BL - Nigerian Law School',
            'Certificate in Corporate Governance',
            'CAC Certified Agent'
        ],
        'specializations': [
            'Business Registration',
            'Corporate Compliance',
            'Regulatory Affairs',
            'Company Secretarial',
            'Legal Documentation'
        ],
        'years_experience': 7,
        'is_featured': False,
        'linkedin': 'https://linkedin.com/in/aisha-mohammed'
    },
    {
        'first_name': 'Samuel',
        'last_name': 'Adeyemi',
        'email': 'samuel.adeyemi@wjprofessionals.com',
        'phone': '+234-809-123-4572',
        'position': 'senior_associate',
        'department': 'audit',
        'photo_path': 'images/staff_6.jpg',  # Placeholder for now
        'bio': '''
        <p>Samuel Adeyemi is a Senior Audit Associate with strong technical skills in audit 
        procedures and financial analysis. He supports our audit team in delivering high-quality 
        audit services to clients across various industries.</p>
        
        <p>Samuel has 5 years of audit experience and has been involved in audits of companies 
        ranging from SMEs to large corporations. He is detail-oriented and committed to 
        maintaining audit quality and professional standards.</p>
        
        <p>He is currently pursuing his chartered accountancy qualification and actively 
        participates in continuing professional development programs.</p>
        ''',
        'qualifications': [
            'ICAN Student (Advanced Level)',
            'B.Sc Accounting - Covenant University',
            'Certificate in Internal Auditing',
            'Risk Management Certification'
        ],
        'specializations': [
            'Financial Audits',
            'Internal Controls Testing',
            'Risk Assessment',
            'Audit Documentation',
            'Compliance Testing'
        ],
        'years_experience': 5,
        'is_featured': False,
        'linkedin': 'https://linkedin.com/in/samuel-adeyemi'
    },
    {
        'first_name': 'Grace',
        'last_name': 'Eze',
        'email': 'grace.eze@wjprofessionals.com',
        'phone': '+234-809-123-4573',
        'position': 'senior_associate',
        'department': 'tax',
        'photo_path': 'images/staff_7.jpg',  # Placeholder for now
        'bio': '''
        <p>Grace Eze is a Senior Tax Associate specializing in individual and small business 
        taxation. She assists clients with tax planning, preparation, and compliance matters, 
        ensuring they meet all their tax obligations efficiently.</p>
        
        <p>With 4 years of experience in taxation, Grace has developed expertise in personal 
        income tax, small business tax planning, and tax compliance. She is known for her 
        client-focused approach and clear communication style.</p>
        
        <p>Grace is passionate about helping small businesses understand their tax obligations 
        and optimize their tax positions through proper planning and compliance.</p>
        ''',
        'qualifications': [
            'CITN Student (Professional Level)',
            'B.Sc Economics - University of Lagos',
            'Certificate in Tax Practice',
            'Payroll Management Certification'
        ],
        'specializations': [
            'Personal Income Tax',
            'Small Business Taxation',
            'Tax Compliance',
            'Payroll Tax',
            'Tax Planning'
        ],
        'years_experience': 4,
        'is_featured': False,
        'linkedin': 'https://linkedin.com/in/grace-eze'
    },
    {
        'first_name': 'Ibrahim',
        'last_name': 'Musa',
        'email': 'ibrahim.musa@wjprofessionals.com',
        'phone': '+234-809-123-4574',
        'position': 'associate',
        'department': 'accounting',
        'photo_path': 'images/staff_8.jpg',  # Placeholder for now
        'bio': '''
        <p>Ibrahim Musa is an Accounting Associate who supports our bookkeeping and financial 
        reporting services. He works closely with clients to maintain accurate financial records 
        and prepare timely financial reports.</p>
        
        <p>With 3 years of experience in accounting, Ibrahim has developed strong skills in 
        bookkeeping, financial statement preparation, and accounting software. He is committed 
        to accuracy and timeliness in all his work.</p>
        
        <p>Ibrahim is pursuing professional accounting qualifications and actively seeks 
        opportunities to expand his knowledge and skills in financial accounting and reporting.</p>
        ''',
        'qualifications': [
            'ANAN Student (Intermediate Level)',
            'HND Accountancy - Federal Polytechnic Bauchi',
            'Certificate in Computerized Accounting',
            'Sage Accounting Certification'
        ],
        'specializations': [
            'Bookkeeping',
            'Financial Statement Preparation',
            'Accounts Reconciliation',
            'Data Entry',
            'Financial Software'
        ],
        'years_experience': 3,
        'is_featured': False,
        'linkedin': 'https://linkedin.com/in/ibrahim-musa'
    }
]

# Rest of your data remains the same...
DEPARTMENTS = [
    {
        'name': 'Management',
        'slug': 'management',
        'description': 'Executive leadership and strategic direction',
        'head_of_department': 'Oluwole Joshua' 
    },
    {
        'name': 'Audit Department',
        'slug': 'audit',
        'description': 'Independent audit and assurance services',
        'head_of_department': 'Adebayo Ogundimu'
    },
    {
        'name': 'Tax Department',
        'slug': 'tax',
        'description': 'Tax planning, preparation and advisory services',
        'head_of_department': 'Fatima Abdullahi'
    },
    {
        'name': 'Accounting Services',
        'slug': 'accounting',
        'description': 'Bookkeeping and financial accounting services',
        'head_of_department': 'Chinedu Okwu'
    },
    {
        'name': 'Business Services',
        'slug': 'business_services',
        'description': 'Business registration and compliance services',
        'head_of_department': 'Aisha Mohammed'
    }
]

POSITIONS = [
    {
        'title': 'Managing Partner',
        'slug': 'managing_partner',
        'level': 'executive',
        'description': 'Chief executive and strategic leader of the firm'
    },
    {
        'title': 'Senior Partner',
        'slug': 'senior_partner',
        'level': 'senior',
        'description': 'Senior leadership with specialized expertise'
    },
    {
        'title': 'Senior Manager',
        'slug': 'senior_manager',
        'level': 'senior',
        'description': 'Department head with management responsibilities'
    },
    {
        'title': 'Manager',
        'slug': 'manager',
        'level': 'mid',
        'description': 'Team leader with supervisory responsibilities'
    },
    {
        'title': 'Senior Associate',
        'slug': 'senior_associate',
        'level': 'mid',
        'description': 'Experienced professional with specialized skills'
    },
    {
        'title': 'Associate',
        'slug': 'associate',
        'level': 'junior',
        'description': 'Professional staff member'
    },
    {
        'title': 'Junior Associate',
        'slug': 'junior_associate',
        'level': 'junior',
        'description': 'Entry-level professional'
    }
]
