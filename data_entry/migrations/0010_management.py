# Generated by Django 5.1.7 on 2025-06-26 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_entry', '0009_timeline_deskripsi_alter_timeline_file_pdf'),
    ]

    operations = [
        migrations.CreateModel(
            name='Management',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namaKelompok', models.TextField()),
                ('deskripsi', models.TextField()),
                ('status', models.TextField()),
            ],
        ),
    ]
