from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Animal, Category, Zone, Blog, Feedback, Quiz, Fact, Favorite
from .forms import RegisterForm, AnimalForm, BlogForm, FeedbackForm, ContactForm
from django.core.mail import send_mail
from django.conf import settings

def contact(request):
    sent = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Save to ContactMessage model
            from .models import ContactMessage
            ContactMessage.objects.create(
                name=cd['name'],
                email=cd['email'],
                subject=cd['subject'],
                urgency=cd.get('urgency', ''),
                message=cd['message']
            )
            # Compose email (optional, still prints to console)
            subject = f"[Virtual Zoo Contact] {cd['subject']} ({cd.get('urgency', 'Normal')})"
            message = f"From: {cd['name']} <{cd['email']}>,\nUrgency: {cd.get('urgency', 'Normal')}\n\n{cd['message']}"
            recipient = getattr(settings, 'ZOO_CONTACT_EMAIL', None) or getattr(settings, 'DEFAULT_FROM_EMAIL', None)
            if recipient:
                send_mail(subject, message, cd['email'], [recipient])
            sent = True
    else:
        form = ContactForm()
    return render(request, 'zoo/contact.html', {'form': form, 'sent': sent})
from .decorators import role_required


def home(request):
    featured = Animal.objects.all().order_by('-created_at')[:6]
    categories = Category.objects.all()
    facts = Fact.objects.all()[:3]
    blogs = Blog.objects.filter(approved=True).order_by('-date_posted')[:3]
    q = request.GET.get('q')
    if q:
        animals = Animal.objects.filter(name__icontains=q) | Animal.objects.filter(species__icontains=q)
    else:
        animals = None
    # Show the most recent animals as featured (for the carousel)
    featured_animals = Animal.objects.order_by('-created_at')[:6]
    stats = {
        'animals': Animal.objects.count(),
        'categories': Category.objects.count(),
        'zones': Zone.objects.count(),
        'quizzes': Quiz.objects.count(),
        'blogs': Blog.objects.count(),
        'feedback': Feedback.objects.count(),
    }
    feedbacks = Feedback.objects.order_by('-created_at')[:5]
    from datetime import datetime
    year = datetime.now().year
    return render(request, 'zoo/home.html', {
        'featured': featured_animals,
        'categories': categories,
        'facts': facts,
        'blogs': blogs,
        'animals': animals,
        'stats': stats,
        'feedbacks': feedbacks,
        'year': year,
    })


def category_list(request, slug=None):
    category = None
    animals = None
    if slug:
        category = get_object_or_404(Category, slug=slug)
        animals = category.animals.all()
    else:
        animals = Animal.objects.all()
    return render(request, 'zoo/animal_list.html', {'animals': animals, 'category': category})


def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    is_fav = False
    if request.user.is_authenticated:
        is_fav = Favorite.objects.filter(user=request.user, animal=animal).exists()
    return render(request, 'zoo/animal_detail.html', {'animal': animal, 'is_fav': is_fav})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # This will save the user with the password from the form
            # Always update profile with correct role and age
            from .models import Profile
            profile = user.profile
            profile.role = form.cleaned_data.get('role')
            profile.age = form.cleaned_data.get('age')
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def favorite_toggle(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, animal=animal)
    if not created:
        fav.delete()
    return redirect('animal_detail', pk=pk)


@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('animal')
    return render(request, 'zoo/favorites.html', {'favorites': favorites})


@login_required
def dashboard(request):
    profile = getattr(request.user, 'profile', None)
    role = profile.role if profile else 'visitor'
    animal_count = Animal.objects.count()
    category_count = Category.objects.count()
    zone_count = Zone.objects.count()
    blog_count = Blog.objects.count()
    recent_animals = Animal.objects.order_by('-created_at')[:5]
    recent_blogs = Blog.objects.order_by('-date_posted')[:5]
    most_viewed_animals = Animal.objects.order_by('-view_count')[:5]
    recent_feedback = Feedback.objects.order_by('-created_at')[:5]
    import json
    categories = Category.objects.all()
    category_labels_json = json.dumps([cat.name for cat in categories])
    category_counts_json = json.dumps([cat.animals.count() for cat in categories])
    context = {
        'role': role,
        'animal_count': animal_count,
        'category_count': category_count,
        'zone_count': zone_count,
        'blog_count': blog_count,
        'recent_animals': recent_animals,
        'recent_blogs': recent_blogs,
        'most_viewed_animals': most_viewed_animals,
        'recent_feedback': recent_feedback,
        'category_labels_json': category_labels_json,
        'category_counts_json': category_counts_json,
    }
    return render(request, 'zoo/dashboard.html', context)


@role_required(['admin', 'zookeeper'])
def manage_animals(request):
    animals = Animal.objects.all().order_by('-created_at')
    return render(request, 'zoo/manage_animals.html', {'animals': animals})


@role_required(['admin', 'zookeeper'])
def animal_add(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Animal created successfully.')
            return redirect('manage_animals')
    else:
        form = AnimalForm()
    return render(request, 'zoo/animal_form.html', {'form': form, 'action': 'Add'})


@role_required(['admin', 'zookeeper'])
def animal_edit(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Animal updated successfully.')
            return redirect('manage_animals')
    else:
        form = AnimalForm(instance=animal)
    return render(request, 'zoo/animal_form.html', {'form': form, 'action': 'Edit', 'animal': animal})


@role_required(['admin', 'zookeeper'])
def animal_delete(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if request.method == 'POST':
        animal.delete()
        messages.success(request, 'Animal deleted.')
        return redirect('manage_animals')
    return render(request, 'zoo/animal_confirm_delete.html', {'animal': animal})


@role_required(['educator'])
def blog_add(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog post created and pending approval.')
            return redirect('dashboard')
    else:
        form = BlogForm()
    return render(request, 'zoo/blog_form.html', {'form': form, 'action': 'Add'})


@role_required(['educator'])
def blog_edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated.')
            return redirect('dashboard')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'zoo/blog_form.html', {'form': form, 'action': 'Edit', 'blog': blog})


@role_required(['educator'])
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Blog post deleted.')
        return redirect('dashboard')
    return render(request, 'zoo/blog_confirm_delete.html', {'blog': blog})


def categories(request):
    categories = Category.objects.all()
    return render(request, 'zoo/category_list.html', {'categories': categories})


def zone_map(request):
    zones = Zone.objects.all()
    return render(request, 'zoo/zone_map.html', {'zones': zones})


def take_quiz(request):
    from .models import Quiz
    quizzes = Quiz.objects.all()[:5]
    quiz_count = quizzes.count()
    feedback = None
    results = {}
    if request.method == 'POST':
        score = 0
        total = quizzes.count()
        for quiz in quizzes:
            user_answer = request.POST.get(f'quiz_{quiz.id}')
            if user_answer:
                is_correct = user_answer.strip() == quiz.correct_answer.strip()
                results[quiz.id] = {
                    'question': quiz.question,
                    'user_answer': user_answer,
                    'correct_answer': quiz.correct_answer,
                    'is_correct': is_correct
                }
                if is_correct:
                    score += 1
            else:
                results[quiz.id] = {
                    'question': quiz.question,
                    'user_answer': None,
                    'correct_answer': quiz.correct_answer,
                    'is_correct': False
                }
        feedback = {
            'score': score,
            'total': total
        }
    return render(request, 'zoo/quiz.html', {
        'quizzes': quizzes,
        'quiz_count': quiz_count,
        'results': results,
        'feedback': feedback
    })


def blog_list(request):
    from .models import Blog
    blogs = Blog.objects.filter(approved=True).order_by('-date_posted')
    return render(request, 'zoo/blog_list.html', {'blogs': blogs})


def blog_detail(request, pk):
    from .models import Blog
    blog = Blog.objects.get(pk=pk)
    return render(request, 'zoo/blog_detail.html', {'blog': blog})


@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('dashboard')
    else:
        form = FeedbackForm()
    return render(request, 'zoo/feedback_form.html', {'form': form})


@role_required(['admin'])
def feedback_list(request):
    feedbacks = Feedback.objects.select_related('user').order_by('-created_at')
    return render(request, 'zoo/feedback_list.html', {'feedbacks': feedbacks})
