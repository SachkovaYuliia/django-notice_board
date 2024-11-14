from django.urls import path
from . import views

urlpatterns = [
    path('recent_ads/', views.recent_ads, name='recent_ads'),
    path('active_ads/', views.active_ads_view, name='active_ads'),
]