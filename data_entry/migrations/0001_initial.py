# Generated by Django 5.1.7 on 2025-03-19 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pengguna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
                ('address_1', models.TextField()),
                ('address_2', models.TextField(blank=True, null=True)),
                ('city', models.CharField(help_text='Enter your city', max_length=20)),
                ('state', models.TextField()),
                ('zip_code', models.CharField(max_length=7)),
                ('tanggal_join', models.DateField(auto_now=True)),
            ],
        ),
    ]
