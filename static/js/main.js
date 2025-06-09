/**
 * WJ Professionals Main JavaScript
 * ================================
 * Main functionality and interactions for the website
 */

(function() {
    'use strict';

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        initializeApp();
    });

    /**
     * Initialize all app functionality
     */
    function initializeApp() {
        initializeNavigation();
        initializeScrollEffects();
        initializeForms();
        initializeModals();
        initializeTooltips();
        initializeAnimations();
        initializeSearch();
        initializeLazyLoading();
        initializeAnalytics();
    }

    /**
     * Navigation functionality
     */
    function initializeNavigation() {
        const navbar = document.querySelector('.navbar');
        const navbarToggler = document.querySelector('.navbar-toggler');
        const navbarCollapse = document.querySelector('.navbar-collapse');

        // Navbar scroll effect
        let lastScrollTop = 0;
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (navbar) {
                if (scrollTop > 100) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }

                // Hide navbar on scroll down, show on scroll up
                if (scrollTop > lastScrollTop && scrollTop > 200) {
                    navbar.style.transform = 'translateY(-100%)';
                } else {
                    navbar.style.transform = 'translateY(0)';
                }
                lastScrollTop = scrollTop;
            }
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                if (!navbarCollapse.contains(event.target) && !navbarToggler.contains(event.target)) {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                        toggle: false
                    });
                    bsCollapse.hide();
                }
            }
        });

        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    const offsetTop = target.offsetTop - (navbar ? navbar.offsetHeight : 0);
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    /**
     * Scroll effects and animations
     */
    function initializeScrollEffects() {
        // Intersection Observer for animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                    
                    // Add specific animation classes
                    if (entry.target.classList.contains('fade-in-up')) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }
                    
                    if (entry.target.classList.contains('fade-in-left')) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateX(0)';
                    }
                    
                    if (entry.target.classList.contains('fade-in-right')) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateX(0)';
                    }
                }
            });
        }, observerOptions);

        // Observe elements with animation classes
        document.querySelectorAll('.fade-in-up, .fade-in-left, .fade-in-right').forEach(el => {
            // Set initial state
            el.style.opacity = '0';
            if (el.classList.contains('fade-in-up')) {
                el.style.transform = 'translateY(30px)';
            } else if (el.classList.contains('fade-in-left')) {
                el.style.transform = 'translateX(-30px)';
            } else if (el.classList.contains('fade-in-right')) {
                el.style.transform = 'translateX(30px)';
            }
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            
            observer.observe(el);
        });

        // Parallax effect for hero sections
        const heroSections = document.querySelectorAll('.hero-section, .page-header');
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            heroSections.forEach(section => {
                const rate = scrolled * -0.5;
                section.style.transform = `translateY(${rate}px)`;
            });
        });
    }

    /**
     * Form enhancements
     */
    function initializeForms() {
        // Form validation
        const forms = document.querySelectorAll('.needs-validation');
        forms.forEach(form => {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });

        // Real-time validation
        const inputs = document.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });

            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    validateField(this);
                }
            });
        });

        // File upload preview
        const fileInputs = document.querySelectorAll('input[type="file"]');
        fileInputs.forEach(input => {
            input.addEventListener('change', function() {
                handleFilePreview(this);
            });
        });

        // Auto-resize textareas
        const textareas = document.querySelectorAll('textarea');
        textareas.forEach(textarea => {
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = this.scrollHeight + 'px';
            });
        });
    }

    /**
     * Validate individual form field
     */
    function validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        // Required validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'This field is required.';
        }

        // Email validation
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                errorMessage = 'Please enter a valid email address.';
            }
        }

        // Phone validation
        // Phone validation
        if (field.type === 'tel' && value) {
            const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
            if (!phoneRegex.test(value.replace(/[\s\-\(\)]/g, ''))) {
                isValid = false;
                errorMessage = 'Please enter a valid phone number.';
            }
        }

        // Password validation
        if (field.type === 'password' && value) {
            if (value.length < 8) {
                isValid = false;
                errorMessage = 'Password must be at least 8 characters long.';
            }
        }

        // Update field state
        if (isValid) {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
        } else {
            field.classList.remove('is-valid');
            field.classList.add('is-invalid');
        }

        // Update error message
        const errorElement = field.parentNode.querySelector('.invalid-feedback');
        if (errorElement) {
            errorElement.textContent = errorMessage;
        }

        return isValid;
    }

    /**
     * Handle file upload preview
     */
    function handleFilePreview(input) {
        const file = input.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = input.parentNode.querySelector('.file-preview');
                if (preview) {
                    if (file.type.startsWith('image/')) {
                        preview.innerHTML = `<img src="${e.target.result}" alt="Preview" class="img-thumbnail" style="max-width: 200px;">`;
                    } else {
                        preview.innerHTML = `<div class="file-info"><i class="fas fa-file"></i> ${file.name}</div>`;
                    }
                }
            };
            reader.readAsDataURL(file);
        }
    }

    /**
     * Modal functionality
     */
    function initializeModals() {
        // Auto-focus first input in modals
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.addEventListener('shown.bs.modal', function() {
                const firstInput = this.querySelector('input, textarea, select');
                if (firstInput) {
                    firstInput.focus();
                }
            });
        });

        // Confirm dialogs
        const confirmButtons = document.querySelectorAll('[data-confirm]');
        confirmButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                const message = this.getAttribute('data-confirm');
                if (!confirm(message)) {
                    e.preventDefault();
                }
            });
        });
    }

    /**
     * Initialize tooltips and popovers
     */
    function initializeTooltips() {
        // Initialize Bootstrap tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });

        // Initialize Bootstrap popovers
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(function(popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }

    /**
     * Animation utilities
     */
    function initializeAnimations() {
        // Counter animation
        const counters = document.querySelectorAll('.counter');
        const counterObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        });

        counters.forEach(counter => {
            counterObserver.observe(counter);
        });

        // Progress bar animation
        const progressBars = document.querySelectorAll('.progress-bar');
        const progressObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const progressBar = entry.target;
                    const width = progressBar.getAttribute('data-width') || progressBar.style.width;
                    progressBar.style.width = '0%';
                    setTimeout(() => {
                        progressBar.style.width = width;
                    }, 100);
                    progressObserver.unobserve(progressBar);
                }
            });
        });

        progressBars.forEach(bar => {
            progressObserver.observe(bar);
        });
    }

    /**
     * Animate counter numbers
     */
    function animateCounter(element) {
        const target = parseInt(element.getAttribute('data-target')) || parseInt(element.textContent);
        const duration = parseInt(element.getAttribute('data-duration')) || 2000;
        const increment = target / (duration / 16);
        let current = 0;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current);
        }, 16);
    }

    /**
     * Search functionality
     */
    function initializeSearch() {
        const searchInputs = document.querySelectorAll('.search-input');
        searchInputs.forEach(input => {
            let searchTimeout;
            
            input.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                const query = this.value.trim();
                
                if (query.length >= 2) {
                    searchTimeout = setTimeout(() => {
                        performSearch(query, this);
                    }, 300);
                } else {
                    clearSearchResults(this);
                }
            });
        });

        // Search suggestions
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.search-container')) {
                document.querySelectorAll('.search-results').forEach(results => {
                    results.style.display = 'none';
                });
            }
        });
    }

    /**
     * Perform search operation
     */
    function performSearch(query, input) {
        const searchContainer = input.closest('.search-container');
        const resultsContainer = searchContainer.querySelector('.search-results');
        
        if (!resultsContainer) return;

        // Show loading state
        resultsContainer.innerHTML = '<div class="search-loading">Searching...</div>';
        resultsContainer.style.display = 'block';

        // Simulate API call (replace with actual search endpoint)
        setTimeout(() => {
            const mockResults = [
                { title: 'Tax Planning Services', url: '/services/tax-planning/' },
                { title: 'Business Consulting', url: '/services/consulting/' },
                { title: 'Financial Auditing', url: '/services/auditing/' }
            ].filter(item => item.title.toLowerCase().includes(query.toLowerCase()));

            displaySearchResults(mockResults, resultsContainer);
        }, 500);
    }

    /**
     * Display search results
     */
    function displaySearchResults(results, container) {
        if (results.length === 0) {
            container.innerHTML = '<div class="search-no-results">No results found</div>';
            return;
        }

        const html = results.map(result => 
            `<a href="${result.url}" class="search-result-item">
                <i class="fas fa-search me-2"></i>${result.title}
            </a>`
        ).join('');

        container.innerHTML = html;
    }

    /**
     * Clear search results
     */
    function clearSearchResults(input) {
        const searchContainer = input.closest('.search-container');
        const resultsContainer = searchContainer.querySelector('.search-results');
        if (resultsContainer) {
            resultsContainer.style.display = 'none';
        }
    }

    /**
     * Lazy loading for images
     */
    function initializeLazyLoading() {
        const images = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.getAttribute('data-src');
                    img.classList.add('loaded');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => {
            imageObserver.observe(img);
        });
    }

    /**
     * Analytics and tracking
     */
    function initializeAnalytics() {
        // Track button clicks
        document.querySelectorAll('.btn[data-track]').forEach(button => {
            button.addEventListener('click', function() {
                const action = this.getAttribute('data-track');
                trackEvent('button_click', action);
            });
        });

        // Track form submissions
        document.querySelectorAll('form[data-track]').forEach(form => {
            form.addEventListener('submit', function() {
                const formName = this.getAttribute('data-track');
                trackEvent('form_submit', formName);
            });
        });

        // Track page scroll depth
        let maxScroll = 0;
        window.addEventListener('scroll', throttle(function() {
            const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
            if (scrollPercent > maxScroll) {
                maxScroll = scrollPercent;
                if (maxScroll % 25 === 0) { // Track at 25%, 50%, 75%, 100%
                    trackEvent('scroll_depth', `${maxScroll}%`);
                }
            }
        }, 1000));
    }

    /**
     * Track events (replace with your analytics provider)
     */
    function trackEvent(action, label) {
        // Google Analytics 4
        if (typeof gtag !== 'undefined') {
            gtag('event', action, {
                'event_label': label,
                'event_category': 'engagement'
            });
        }

        // Console log for development
        console.log('Event tracked:', action, label);
    }

    /**
     * Utility functions
     */
    
    // Throttle function
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // Debounce function
    function debounce(func, wait, immediate) {
        let timeout;
        return function() {
            const context = this, args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    }

    // Get cookie value
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Set cookie
    function setCookie(name, value, days) {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "") + expires + "; path=/";
    }

    // Show notification
    function showNotification(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show notification`;
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Add to page
        const container = document.querySelector('.notification-container') || document.body;
        container.appendChild(notification);

        // Auto-remove after duration
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, duration);
    }

    // AJAX helper
    function makeRequest(url, options = {}) {
        const defaults = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        };

        const config = Object.assign({}, defaults, options);

        return fetch(url, config)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .catch(error => {
                console.error('Request failed:', error);
                showNotification('An error occurred. Please try again.', 'danger');
                throw error;
            });
    }

    // Format currency
    function formatCurrency(amount, currency = 'USD') {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency
        }).format(amount);
    }

    // Format date
    function formatDate(date, options = {}) {
        const defaults = {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        };
        const config = Object.assign({}, defaults, options);
        return new Intl.DateTimeFormat('en-US', config).format(new Date(date));
    }

    // Expose utility functions globally
    window.WJProfessionals = {
        showNotification,
        makeRequest,
        formatCurrency,
        formatDate,
        getCookie,
        setCookie,
        trackEvent
    };

    // Handle page visibility changes
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            // Page is hidden
            trackEvent('page_hidden', window.location.pathname);
        } else {
            // Page is visible
            trackEvent('page_visible', window.location.pathname);
        }
    });

    // Handle online/offline status
    window.addEventListener('online', function() {
        showNotification('Connection restored', 'success');
    });

    window.addEventListener('offline', function() {
        showNotification('Connection lost. Some features may not work.', 'warning');
    });

    // Performance monitoring
    window.addEventListener('load', function() {
        // Log page load time
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        console.log('Page load time:', loadTime + 'ms');
        
        // Track slow pages (over 3 seconds)
        if (loadTime > 3000) {
            trackEvent('slow_page_load', window.location.pathname);
        }
    });

})();

/**
 * Additional component-specific JavaScript
 */

// Contact form enhancements
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.querySelector('#contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            
            // Show loading state
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
            submitButton.disabled = true;
            
            // Submit form
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Message sent successfully!', 'success');
                    this.reset();
                } else {
                    showNotification('Error sending message. Please try again.', 'danger');
                }
            })
            .catch(error => {
                showNotification('Error sending message. Please try again.', 'danger');
            })
            .finally(() => {
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            });
        });
    }
});

// Document download tracking
document.addEventListener('click', function(e) {
    if (e.target.closest('a[href*="download"]')) {
        const link = e.target.closest('a');
        const documentName = link.getAttribute('data-document') || 'unknown';
        trackEvent('document_download', documentName);
    }
});

// Service inquiry tracking
document.addEventListener('click', function(e) {
    if (e.target.closest('.service-inquiry-btn')) {
        const service = e.target.closest('.service-inquiry-btn').getAttribute('data-service');
        trackEvent('service_inquiry', service);
    }
});

// Floating Logo Functionality
document.addEventListener('DOMContentLoaded', function() {
    const floatingLogo = document.getElementById('floatingLogo');
    let lastScrollTop = 0;
    
    // Show/hide floating logo based on scroll
    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 200) {
            floatingLogo.classList.add('visible');
        } else {
            floatingLogo.classList.remove('visible');
        }
        
        lastScrollTop = scrollTop;
    });
    
    // Click to scroll to top
    floatingLogo.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Add active class to current nav item
    const currentLocation = location.pathname;
    const navLinks = document.querySelectorAll('.nav-link-modern');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
            link.style.background = 'rgba(255,193,7,0.2)';
            link.style.color = '#ffc107';
        }
    });
    
    // Smooth dropdown animations
    const dropdowns = document.querySelectorAll('.dropdown-menu-modern');
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('show.bs.dropdown', function() {
            this.style.animation = 'fadeInUp 0.3s ease-out';
        });
    });
});

// Add fadeInUp animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);
