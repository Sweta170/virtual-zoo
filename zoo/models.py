
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class ContactMessage(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()
    subject = models.CharField(max_length=120)
    urgency = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} from {self.name} ({self.email})"


class Profile(models.Model):
    ROLE_CHOICES = [
        ('visitor', 'Visitor'),
        ('admin', 'Admin'),
        ('zookeeper', 'Zookeeper'),
        ('educator', 'Educator'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='visitor')
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Category(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=140, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Zone(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    map_location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Animal(models.Model):
    name = models.CharField(max_length=140)
    species = models.CharField(max_length=140, blank=True)
    scientific_name = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='animals')
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    diet = models.CharField(max_length=200, blank=True)
    habitat = models.CharField(max_length=200, blank=True)
    fun_facts = models.TextField(blank=True)
    image = models.ImageField(upload_to='animals/images/', blank=True, null=True)
    sound = models.FileField(upload_to='animals/sounds/', blank=True, null=True)
    video = models.FileField(upload_to='animals/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Fact(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user or 'Anonymous'}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'animal')

    def __str__(self):
        return f"{self.user.username} likes {self.animal.name}"


class Quiz(models.Model):
    question = models.CharField(max_length=400)
    options = models.TextField(help_text='Store options as JSON list or newline-separated')
    correct_answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question
