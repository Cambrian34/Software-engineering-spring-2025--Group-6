# Generated by Django 3.2.9 on 2025-04-22 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20250421_0353'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='checkout_session_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
