
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zoo', '0002_animal_view_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
