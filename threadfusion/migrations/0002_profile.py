# Generated by Django 5.0.4 on 2024-05-27 17:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threadfusion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('fullname', models.CharField(max_length=50)),
                ('profession', models.CharField(max_length=50)),
                ('about', models.TextField()),
                ('linkedin', models.CharField(max_length=100)),
                ('github', models.CharField(max_length=100)),
                ('instagram', models.CharField(max_length=100)),
                ('facebook', models.CharField(max_length=100)),
                ('twitter', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]