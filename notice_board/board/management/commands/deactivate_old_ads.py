from django.core.management.base import BaseCommand
from board.models import Ad
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Deactivate ads older than 30 days'

    def handle(self, *args, **kwargs):
        old_ads = Ad.objects.filter(created_at__lt=timezone.now() - timedelta(days=30), is_active=True)
        old_ads.update(is_active=False)
        self.stdout.write("Deactivated old ads.")