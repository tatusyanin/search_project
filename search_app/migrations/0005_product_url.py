# Generated by Django 5.1.2 on 2024-11-06 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_app', '0004_rename_item_name_favorite_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
