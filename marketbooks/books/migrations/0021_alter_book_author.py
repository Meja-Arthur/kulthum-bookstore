# Generated by Django 5.0.2 on 2024-03-26 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0020_author_alter_book_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=100),
        ),
    ]
