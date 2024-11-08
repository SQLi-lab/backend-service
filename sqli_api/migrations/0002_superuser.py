from django.contrib.auth.hashers import make_password
from django.db import migrations

def create_superuser(apps, schema_editor):
    User = apps.get_model('sqli_api', 'CustomUser')
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create(
            username="Главный Админ",
            study_group="Преподаватель",
            group="admin",
            email="admin@admin.com",
            password=make_password("admin"),  # Hash the password
            is_staff=True,
            is_superuser=True
        )

class Migration(migrations.Migration):

    dependencies = [
        ('sqli_api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
