from django.contrib import admin
from .models import Profile, Category, Ad, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'is_active', 'category')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    actions = ['deactivate_old_ads']

    def deactivate_old_ads(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_old_ads.short_description = "Позначити вибрані оголошення як неактивні"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('ad', 'user', 'created_at')
    search_fields = ('content',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')

