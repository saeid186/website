# Generated by Django 4.0.3 on 2022-09-26 15:37

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, quality=-1, scale=None, size=[500, 500], upload_to='product'),
        ),
    ]
