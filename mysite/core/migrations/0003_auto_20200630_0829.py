# Generated by Django 2.1.3 on 2020-06-30 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_book_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pdf',
            field=models.FileField(upload_to='books/pdfs/', verbose_name='pdf/json/txt'),
        ),
    ]