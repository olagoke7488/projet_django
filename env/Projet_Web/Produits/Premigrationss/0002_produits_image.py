# Generated by Django 4.2.16 on 2025-06-15 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Produits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produits',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
