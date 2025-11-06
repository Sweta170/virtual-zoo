<<<<<<< HEAD
# Virtual Zoo

This is a minimal Django-based Virtual Zoo scaffold implementing:

- Role-based profiles (Visitor, Admin, Zookeeper, Educator)
- Models for Category, Animal, Zone, Blog, Fact, Feedback, Favorite, Quiz
- Basic CRUD via Django Admin
- Frontend templates (home, animal list, animal detail)
- Media upload support (images, sound, video) using Pillow

This project uses SQLite and is intentionally minimal to be extended.

Getting started (Windows PowerShell):

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Run migrations and create superuser

```powershell
python manage.py migrate
python manage.py createsuperuser
```

4. Run the development server

```powershell
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to open the site and http://127.0.0.1:8000/admin/ for the admin panel.

Notes:
- Change SECRET_KEY in `virtualzoo/settings.py` for production.
- Media files are served in DEBUG mode. Configure a proper media/static host for production.
=======
# virtual-zoo
>>>>>>> 8b734f6b7a647ee66580874afa558869a17fe625
