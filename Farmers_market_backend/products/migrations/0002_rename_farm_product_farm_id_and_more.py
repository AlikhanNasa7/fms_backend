# Generated by Django 5.1.3 on 2024-11-23 20:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='farm',
            new_name='farm_id',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='is_active',
            new_name='is_available',
        ),
        migrations.AddField(
            model_name='product',
            name='unit_name',
            field=models.CharField(choices=[('kg', 'kg'), ('pcs', 'pcs'), ('litres', 'litres')], default='kg', max_length=20),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(default='tomato', on_delete=django.db.models.deletion.DO_NOTHING, to='products.subcategory'),
            preserve_default=False,
        ),
    ]
