# Generated by Django 5.1.3 on 2024-11-23 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_orderitem_farm_id_orderitem_unit_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='farm_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='farmer_id',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='total_price',
        ),
        migrations.AddField(
            model_name='delivery',
            name='delivery_id',
            field=models.CharField(default=1, max_length=75, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='delivery_date',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='delivery_method',
            field=models.CharField(choices=[('pickup', 'pickup'), ('courier', 'courier')], default='courier', max_length=20),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='status',
            field=models.CharField(blank=True, choices=[('paid', 'paid'), ('packed', 'packed'), ('on a way', 'on a way'), ('delivered', 'delivered')], default='paid', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order_item_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
