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
    age = forms.IntegerField(required=True, min_value=1, label='Age')

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'age', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            role = self.cleaned_data.get('role')
            age = self.cleaned_data.get('age')
            from .models import Profile
            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = role
            profile.age = age
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
