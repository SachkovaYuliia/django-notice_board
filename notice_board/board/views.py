from django.shortcuts import render
from .models import Ad, Profile
from django.utils import timezone
from datetime import timedelta

def recent_ads(request):
    ads = Ad.objects.filter(created_at__gte=timezone.now() - timedelta(days=30))
    return render(request, 'board/recent_ads.html', {'ads': ads})

def active_ads_view(request):
    ads = Ad.objects.active_ads()  
    return render(request, 'board/active_ads.html', {'ads': ads})