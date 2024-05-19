# Generated by Django 5.0.6 on 2024-05-19 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_book_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='quantity',
            new_name='available_quantity',
        ),
        migrations.AddField(
            model_name='book',
            name='total_quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]