# Generated by Django 4.0.3 on 2022-03-31 08:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0014_alter_category_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='favourite',
            field=models.ManyToManyField(blank=True, related_name='fa_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
