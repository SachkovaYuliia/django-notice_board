from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Ad
from django.utils import timezone
from datetime import timedelta

@receiver(post_save, sender=Ad)
def send_email_on_ad_creation(sender, instance, created, **kwargs):
    if created: 
        send_mail(
            subject="Ваше оголошення створено",
            message=f"Дякуємо, {instance.user.username}, за створення оголошення '{instance.title}'.",
            from_email="admin@mysite.com",
            recipient_list=[instance.user.email],
            fail_silently=False,
        )

@receiver(post_save, sender=Ad)
def deactivate_ad_after_30_days(sender, instance, **kwargs):
    if timezone.now() - instance.created_at >= timedelta(days=30):
            instance.is_active = False
            instance.save()
