# Generated by Django 3.0.2 on 2020-04-28 10:48

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20200428_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='aucBidder',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='auction',
            name='aucIsOpen',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='auction',
            name='aucPrice',
            field=models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='auction',
            name='aucWinner',
            field=models.CharField(max_length=60),
        ),
    ]