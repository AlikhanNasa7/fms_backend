# Generated by Django 5.1.3 on 2024-11-28 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_category_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_urls',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]