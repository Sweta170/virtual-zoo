import os
import urllib.request
from django.core.management.base import BaseCommand
from django.core.files import File as DjangoFile
from django.conf import settings


class Command(BaseCommand):
    help = 'Load demo data: categories, zones, animals, facts and a sample blog.'

    def handle(self, *args, **options):
        from zoo.models import Category, Zone, Animal, Fact, Blog
        from django.contrib.auth.models import User

        self.stdout.write('Creating demo user (if not exists)')
        demo_user, _ = User.objects.get_or_create(username='demo', defaults={'email': 'demo@example.com'})
        demo_user.set_password('demo1234')
        demo_user.save()

        categories = ['Mammals', 'Birds', 'Reptiles', 'Amphibians', 'Fish', 'Insects']
        self.stdout.write('Creating categories...')
        cat_objs = {}
        for name in categories:
            c, _ = Category.objects.get_or_create(name=name, defaults={'description': f'{name} at the Virtual Zoo'})
            cat_objs[name] = c

        self.stdout.write('Creating zones...')
        zones = ['Jungle', 'Desert', 'Ocean', 'Savannah', 'Rainforest']
        zone_objs = {}
        for z in zones:
            obj, _ = Zone.objects.get_or_create(name=z, defaults={'description': f'{z} zone'})
            zone_objs[z] = obj

        # helper to download placeholder image
        def try_download_image(url, dest_path):
            try:
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                urllib.request.urlretrieve(url, dest_path)
                return True
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Could not download image {url}: {e}'))
                return False

        self.stdout.write('Creating animals...')
        animals = [
            {
                'name': 'African Elephant',
                'species': 'Loxodonta africana',
                'scientific_name': 'Loxodonta africana',
                'category': 'Mammals',
                'zone': 'Savannah',
                'description': 'Large herbivore with tusks.',
                'diet': 'Herbivore',
                'habitat': 'Savannah',
                'fun_facts': 'They have strong social bonds.'
            },
            {
                'name': 'Bald Eagle',
                'species': 'Haliaeetus leucocephalus',
                'scientific_name': 'Haliaeetus leucocephalus',
                'category': 'Birds',
                'zone': 'Rainforest',
                'description': 'A large bird of prey.',
                'diet': 'Carnivore',
                'habitat': 'Near water',
                'fun_facts': 'National bird of the United States.'
            },
            {
                'name': 'Green Sea Turtle',
                'species': 'Chelonia mydas',
                'scientific_name': 'Chelonia mydas',
                'category': 'Fish',
                'zone': 'Ocean',
                'description': 'Marine turtle that feeds on seagrass.',
                'diet': 'Herbivore',
                'habitat': 'Oceans',
                'fun_facts': 'Can live for decades.'
            },
            {
                'name': 'Komodo Dragon',
                'species': 'Varanus komodoensis',
                'scientific_name': 'Varanus komodoensis',
                'category': 'Reptiles',
                'zone': 'Desert',
                'description': 'Largest living species of lizard.',
                'diet': 'Carnivore',
                'habitat': 'Tropical savannahs',
                'fun_facts': 'Has venom glands.'
            },
            {
                'name': 'Poison Dart Frog',
                'species': 'Dendrobatidae',
                'scientific_name': 'Dendrobatidae',
                'category': 'Amphibians',
                'zone': 'Jungle',
                'description': 'Colorful small frog.',
                'diet': 'Insectivore',
                'habitat': 'Tropical rainforests',
                'fun_facts': 'Some species are poisonous.'
            },
        ]

        # placeholder image URLs (small images)
        placeholder_urls = {
            'African Elephant': 'https://placehold.co/600x400?text=Elephant',
            'Bald Eagle': 'https://placehold.co/600x400?text=Bald+Eagle',
            'Green Sea Turtle': 'https://placehold.co/600x400?text=Sea+Turtle',
            'Komodo Dragon': 'https://placehold.co/600x400?text=Komodo+Dragon',
            'Poison Dart Frog': 'https://placehold.co/600x400?text=Poison+Dart+Frog',
        }

        for a in animals:
            obj, created = Animal.objects.get_or_create(
                name=a['name'],
                defaults={
                    'species': a['species'],
                    'scientific_name': a['scientific_name'],
                    'category': cat_objs.get(a['category']),
                    'zone': zone_objs.get(a['zone']),
                    'description': a['description'],
                    'diet': a['diet'],
                    'habitat': a['habitat'],
                    'fun_facts': a['fun_facts'],
                }
            )
            if created:
                # try to download image into MEDIA_ROOT/animals/images/
                url = placeholder_urls.get(a['name'])
                if url and getattr(settings, 'MEDIA_ROOT', None):
                    fname = f"animals/images/{a['name'].replace(' ', '_')}.jpg"
                    dest = os.path.join(settings.MEDIA_ROOT, fname)
                    ok = try_download_image(url, dest)
                    if ok:
                        with open(dest, 'rb') as f:
                            obj.image.save(os.path.basename(dest), DjangoFile(f), save=True)
                self.stdout.write(self.style.SUCCESS(f'Created animal: {obj.name}'))
            else:
                self.stdout.write(f'Animal exists: {obj.name}')

        self.stdout.write('Creating facts...')
        facts = [
            ('Elephants can recognize themselves in mirrors', 'Elephants show self-awareness.'),
            ('Bird migration', 'Many birds migrate thousands of miles.'),
        ]
        for title, content in facts:
            Fact.objects.get_or_create(title=title, defaults={'content': content})

        self.stdout.write('Creating a sample blog...')
        Blog.objects.get_or_create(title='Welcome to the Virtual Zoo', defaults={'content': 'This is a demo blog post.', 'author': demo_user, 'approved': True})

        # Add demo quizzes
        from zoo.models import Quiz
        Quiz.objects.get_or_create(
            question="Which animal is known as the king of the jungle?",
            options="Lion\nTiger\nElephant\nGiraffe",
            correct_answer="Lion"
        )
        Quiz.objects.get_or_create(
            question="Which animal can fly?",
            options="Penguin\nEagle\nOstrich\nElephant",
            correct_answer="Eagle"
        )
        Quiz.objects.get_or_create(
            question="Which animal is the largest land mammal?",
            options="Lion\nElephant\nGiraffe\nRhino",
            correct_answer="Elephant"
        )

        self.stdout.write(self.style.SUCCESS('Demo data loaded. Demo user: demo / demo1234'))