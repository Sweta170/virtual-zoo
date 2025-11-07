from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Animal, Category, Blog, Profile, Feedback


# Contact form for zookeeper contact
class ContactForm(forms.Form):
    SUBJECT_CHOICES = [
        ("General", "General Inquiry"),
        ("Animal Care", "Animal Care"),
        ("Lost & Found", "Lost & Found"),
        ("Emergency", "Emergency"),
        ("Other", "Other"),
    ]
    URGENCY_CHOICES = [
        ("Normal", "Normal"),
        ("Urgent", "Urgent"),
    ]
    name = forms.CharField(max_length=60, required=True, label="Your Name")
    email = forms.EmailField(required=True, label="Your Email")
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, required=True)
    urgency = forms.ChoiceField(choices=URGENCY_CHOICES, required=False, initial="Normal")
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}), required=True, label="Message")
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Animal, Category, Blog, Profile, Feedback


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, initial='visitor')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super().save(commit=commit)
        role = self.cleaned_data.get('role')
        if commit:
            profile = Profile.objects.get(user=user)
            profile.role = role
            profile.save()
        return user


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'species', 'scientific_name', 'category', 'zone', 'description', 'diet', 'habitat', 'fun_facts', 'image', 'sound', 'video']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message', 'rating']
