# Generated by Django 3.0.2 on 2020-04-28 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_remove_auction_itemid'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='itemID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='myapp.Item'),
        ),
    ]
