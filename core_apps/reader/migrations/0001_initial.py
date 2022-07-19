# Generated by Django 4.0.6 on 2022-07-19 19:37

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('author', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=20)),
                ('rating', models.IntegerField()),
                ('cover', models.ImageField(default='bitcoin.png', upload_to='images/')),
                ('upload', models.FileField(null=True, storage=django.core.files.storage.FileSystemStorage(location='/home/tornado/PycharmProjects/mysite/private'), upload_to='')),
                ('description', models.TextField()),
                ('notes', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]