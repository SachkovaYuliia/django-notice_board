from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.core.mail import send_mail

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def active_ads_count(self):
        return self.ad_set.filter(is_active=True).count()

class AdManager(models.Manager):
    def active_ads(self):
        return self.filter(is_active=True)

    def ads_last_month(self):
        return self.filter(created_at__gte=timezone.now() - timedelta(days=30))

class Ad(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    objects = AdManager()  

    def __str__(self):
        return self.title

    def short_description(self):
        return self.description[:100] + "..." if len(self.description) > 100 else self.description

    def comments_count(self):
        return self.comments.count()
    
    def deactivate_after_30_days(self):
        if timezone.now() - self.created_at >= timedelta(days=30):
            self.is_active = False
            self.save()

    def clean(self):
        if self.price <= 0:
            raise ValidationError("Ціна має бути додатним числом.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

@receiver(post_save, sender=Ad)
def send_email_on_ad_creation(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Ваше оголошення створено!',
            f'Дякуємо за створення оголошення: {instance.title}',
            'admin@google.com',
            [instance.user.email],
            fail_silently=True,
        )

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.ad.title}"
