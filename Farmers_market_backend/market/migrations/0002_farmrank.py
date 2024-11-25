# Generated by Django 5.1.3 on 2024-11-23 20:17

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
        ('users', '0002_customuser_is_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmRank',
            fields=[
                ('rank_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('value', models.DecimalField(decimal_places=1, max_digits=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('buyer_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.buyer')),
                ('farm_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.farm')),
            ],
        ),
    ]
