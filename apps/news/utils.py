# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web_updated_temp\wj_professionals\apps\news\utils.py
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import NewsletterSubscriber

def broadcast_new_article(article):
    # Only to confirmed & active subscribers
    subs = NewsletterSubscriber.objects.filter(is_active=True, confirmed=True)
    if not subs.exists():
        return 0
    sent = 0
    for s in subs:
        unsubscribe_url = f"{settings.SITE_URL}{reverse('news:newsletter_unsubscribe', args=[s.confirmation_token])}"
        article_url = f"{settings.SITE_URL}{article.get_absolute_url()}"
        context = {
            'subscriber': s,
            'article': article,
            'article_url': article_url,
            'unsubscribe_url': unsubscribe_url,
        }
        subject = f"New update: {article.title}"
        plain = render_to_string('news/emails/new_article.txt', context)
        html = render_to_string('news/emails/new_article.html', context)
        try:
            send_mail(subject, plain, settings.EMAIL_HOST_USER, [s.email], html_message=html, fail_silently=False)
            sent += 1
        except Exception:
            pass
    return sent
