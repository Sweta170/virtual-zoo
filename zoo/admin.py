from django.contrib import admin
from .models import (
    Profile, Category, Animal, Fact, Blog, Zone, Feedback, Favorite, Quiz, ContactMessage
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'category', 'zone', 'created_at')
    list_filter = ('category', 'zone')
    search_fields = ('name', 'species', 'scientific_name')


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'approved')
    list_filter = ('approved',)
    search_fields = ('title', 'content')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'animal')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('question',)

admin.site.register(ContactMessage)
