# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\core\fixtures\news_data.py
"""
Sample Data
===========
Additional sample data for news, testimonials, etc.
"""

NEWS_ARTICLES_DATA = [
    {
        'title': 'New VAT Rate Changes: What Nigerian Businesses Need to Know',
        'slug': 'new-vat-rate-changes-nigerian-businesses',
        'article_type': 'news',
        'excerpt': 'The Federal Government has announced changes to VAT rates. Here\'s how it affects your business and what you need to do to stay compliant.',
        'content': '''
        <p>The Nigerian Federal Government has announced significant changes to the Value Added Tax (VAT) structure, 
        effective from January 2024. These changes will impact businesses across all sectors, and it's crucial for 
        business owners to understand the implications.</p>
        
        <h3>Key Changes</h3>
        <ul>
            <li>Standard VAT rate increased from 7.5% to 10%</li>
            <li>New exemptions for essential goods and services</li>
            <li>Modified registration threshold for small businesses</li>
            <li>Enhanced digital filing requirements</li>
        </ul>
        
        <h3>Impact on Businesses</h3>
        <p>The VAT rate increase will affect pricing strategies, cash flow, and compliance requirements. Businesses 
        need to review their pricing models and ensure their accounting systems are updated to reflect the new rates.</p>
        
        <h3>Action Items</h3>
        <ol>
            <li>Update your accounting software with new VAT rates</li>
            <li>Review and adjust your pricing strategy</li>
            <li>Ensure compliance with new filing requirements</li>
            <li>Consider the impact on cash flow and budgeting</li>
        </ol>
        
        <p>At WJ Professionals, we're here to help you navigate these changes. Contact us for personalized advice 
        on how these VAT changes affect your specific business situation.</p>
        ''',
        'status': 'published',
        'is_featured': True,
        'is_breaking': False,
        'tags': ['VAT', 'Tax Changes', 'Business Compliance', 'Nigeria']
    },
    {
        'title': 'Digital Transformation in Accounting: Embracing Technology for Better Financial Management',
        'slug': 'digital-transformation-accounting-technology',
        'article_type': 'insight',
        'excerpt': 'How modern accounting firms are leveraging technology to provide better services and help clients make more informed financial decisions.',
        'content': '''
        <p>The accounting industry is undergoing a digital revolution. Cloud-based accounting software, artificial 
        intelligence, and automation are transforming how financial services are delivered and consumed.</p>
        
        <h3>Benefits of Digital Accounting</h3>
        <ul>
            <li>Real-time financial reporting</li>
            <li>Improved accuracy and reduced errors</li>
            <li>Better collaboration between clients and accountants</li>
            <li>Enhanced security and data backup</li>
            <li>Cost-effective solutions for businesses of all sizes</li>
        </ul>
        
        <h3>Key Technologies</h3>
        <p>Modern accounting practices incorporate various technologies including cloud computing, machine learning 
        for data analysis, mobile applications for on-the-go access, and integrated business management systems.</p>
        
        <p>At WJ Professionals, we've embraced these technologies to provide our clients with cutting-edge financial 
        services that are both efficient and secure.</p>
        ''',
        'status': 'published',
        'is_featured': False,
        'is_breaking': False,
        'tags': ['Digital Transformation', 'Accounting Technology', 'Cloud Computing', 'Financial Management']
    },
    {
        'title': 'Tax Planning Strategies for Small Businesses in Nigeria',
        'slug': 'tax-planning-strategies-small-businesses-nigeria',
        'article_type': 'guide',
        'excerpt': 'Essential tax planning strategies that can help small businesses in Nigeria minimize their tax burden while staying compliant with FIRS regulations.',
        'content': '''
        <p>Effective tax planning is crucial for small businesses in Nigeria. With proper strategies, businesses can 
        minimize their tax burden while ensuring full compliance with Federal Inland Revenue Service (FIRS) regulations.</p>
        
        <h3>Key Tax Planning Strategies</h3>
        
        <h4>1. Choose the Right Business Structure</h4>
        <p>The structure of your business (sole proprietorship, partnership, or limited company) significantly 
        impacts your tax obligations. Each structure has different tax implications and benefits.</p>
        
        <h4>2. Maximize Allowable Deductions</h4>
        <ul>
            <li>Office rent and utilities</li>
            <li>Professional fees and subscriptions</li>
            <li>Training and development costs</li>
            <li>Equipment and software purchases</li>
            <li>Business travel and entertainment</li>
        </ul>
        
        <h4>3. Timing of Income and Expenses</h4>
        <p>Strategic timing of when you recognize income and claim expenses can help optimize your tax position.</p>
        
        <h4>4. Take Advantage of Tax Incentives</h4>
        <p>The Nigerian government offers various tax incentives for small businesses, including reduced tax rates 
        for companies with turnover below certain thresholds.</p>
        
        <p>For personalized tax planning advice, consult with our experienced tax professionals at WJ Professionals.</p>
        ''',
        'status': 'published',
        'is_featured': True,
        'is_breaking': False,
        'tags': ['Tax Planning', 'Small Business', 'Nigeria', 'FIRS', 'Business Strategy']
    }
]

TESTIMONIALS_DATA = [
    {
        'client_name': 'Adebola Adeyemi',
        'company': 'Adeyemi Trading Company',
        'position': 'Managing Director',
        'content': '''WJ Professionals has been instrumental in helping us navigate the complex Nigerian tax landscape. 
        Their expertise in tax planning saved us over ₦2 million in the first year alone. The team is professional, 
        responsive, and truly understands our business needs.''',
        'rating': 5,
        'is_featured': True,
        'service_category_slug': 'tax-services'
    },
    {
        'client_name': 'Mrs. Kemi Okafor',
        'company': 'Okafor Enterprises Ltd',
        'position': 'CEO',
        'content': '''The audit services provided by WJ Professionals were thorough and professional. They identified 
        several areas for improvement in our financial controls and helped us implement better systems. I highly 
        recommend their services to any business looking for quality audit work.''',
        'rating': 5,
        'is_featured': True,
        'service_category_slug': 'audit-assurance'
    },
    {
        'client_name': 'Mr. Ibrahim Sani',
        'company': 'Sani Construction Ltd',
        'position': 'Financial Controller',
        'content': '''WJ Professionals handled our company registration and ongoing compliance requirements seamlessly. 
        They made the entire process stress-free and ensured we met all regulatory deadlines. Their business advisory 
        services have also been invaluable as we expand our operations.''',
        'rating': 5,
        'is_featured': True,
        'service_category_slug': 'business-registration'
    },
    {
        'client_name': 'Dr. Funmi Adebayo',
        'company': 'Adebayo Medical Centre',
        'position': 'Medical Director',
        'content': '''As a busy medical practitioner, I needed reliable accounting support for my practice. WJ Professionals 
        has been managing our books for over three years now, and their attention to detail and timely reporting has 
        been exceptional. They truly understand the healthcare industry.''',
        'rating': 5,
        'is_featured': False,
        'service_category_slug': 'accounting-services'
    },
    {
        'client_name': 'Mr. Chukwuma Obi',
        'company': 'Obi Tech Solutions',
        'position': 'Founder & CEO',
        'content': '''The financial advisory services from WJ Professionals helped us secure funding for our expansion. 
        Their business plan development and financial projections were instrumental in convincing investors. They are 
        true partners in our business growth.''',
        'rating': 5,
        'is_featured': False,
        'service_category_slug': 'business-advisory'
    }
]

FAQ_DATA = [
    {
        'question': 'What documents do I need for business registration in Nigeria?',
        'answer': '''For business registration in Nigeria, you typically need:
        <ul>
            <li>Completed CAC forms (CAC 1.1 for name reservation, CAC 2.1 for incorporation)</li>
            <li>Memorandum and Articles of Association</li>
            <li>Valid identification of directors and shareholders</li>
            <li>Passport photographs of directors</li>
            <li>Proof of address for registered office</li>
            <li>Statement of share capital and shareholding</li>
        </ul>
        Our team can help you prepare all required documents and guide you through the entire process.''',
        'category': 'business',
        'is_featured': True
    },
    {
        'question': 'How often should I file my tax returns in Nigeria?',
        'answer': '''Tax filing frequency in Nigeria depends on your business type:
        <ul>
            <li><strong>Companies:</strong> Annual returns (within 6 months of year-end)</li>
            <li><strong>VAT:</strong> Monthly returns (by 21st of following month)</li>
            <li><strong>Withholding Tax:</strong> Monthly returns (by 21st of following month)</li>
            <li><strong>PAYE:</strong> Monthly returns for employee taxes</li>
            <li><strong>Personal Income Tax:</strong> Annual returns (by March 31st)</li>
        </ul>
        We help ensure you meet all filing deadlines and remain compliant with FIRS requirements.''',
        'category': 'tax',
        'is_featured': True
    },
    {
        'question': 'What is the difference between bookkeeping and accounting?',
        'answer': '''While often used interchangeably, bookkeeping and accounting serve different purposes:
        
        <strong>Bookkeeping:</strong>
        <ul>
            <li>Recording daily financial transactions</li>
            <li>Maintaining ledgers and journals</li>
            <li>Data entry and organization</li>
            <li>Bank reconciliations</li>
        </ul>
        
        <strong>Accounting:</strong>
        <ul>
            <li>Analyzing and interpreting financial data</li>
            <li>Preparing financial statements</li>
            <li>Tax planning and preparation</li>
            <li>Financial advisory and consulting</li>
        </ul>
        
        We provide both services to give you complete financial management support.''',
        'category': 'accounting',
        'is_featured': True
    },
    {
        'question': 'Do I need an audit for my small business?',
        'answer': '''Audit requirements in Nigeria depend on your company size and type:
        
        <strong>Mandatory Audits:</strong>
        <ul>
            <li>All public companies</li>
            <li>Private companies with turnover above ₦2 billion</li>
            <li>Banks and financial institutions</li>
            <li>Insurance companies</li>
        </ul>
        
        <strong>Optional but Recommended:</strong>
        <ul>
            <li>For loan applications</li>
            <li>For investor relations</li>
            <li>For internal control assessment</li>
            <li>For regulatory compliance</li>
        </ul>
        
        Even if not mandatory, an audit can provide valuable insights into your business operations and financial health.''',
        'category': 'audit',
        'is_featured': True
    }
]
