# Generated by Django 5.1.3 on 2024-11-26 12:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_alter_farmrank_value'),
        ('users', '0003_alter_customuser_role_delete_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farm',
            name='farmer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='farms', to='users.farmer'),
        ),
        migrations.AlterField(
            model_name='farmrank',
            name='buyer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reviews', to='users.buyer'),
        ),
        migrations.AlterField(
            model_name='farmrank',
            name='farm_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rank', to='market.farm'),
        ),
        migrations.CreateModel(
            name='FarmAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_sales', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('products_sold', models.PositiveIntegerField(default=0)),
                ('average_order_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('top_selling_product', models.CharField(blank=True, max_length=255, null=True)),
                ('repeat_buyers_count', models.PositiveIntegerField(default=0)),
                ('monthly_sales', models.JSONField(default=dict)),
                ('gross_profit', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('completed_orders_count', models.PositiveIntegerField(default=0)),
                ('cancelled_orders_count', models.PositiveIntegerField(default=0)),
                ('buyer_feedback_average', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('farm', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='analytics', to='market.farm')),
            ],
        ),
    ]
