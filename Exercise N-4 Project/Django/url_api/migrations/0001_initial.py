# Generated by Django 4.1.6 on 2023-03-17 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=100, unique=True)),
                ('is_premium_client', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_link', models.CharField(max_length=250)),
                ('shortened_link', models.CharField(max_length=100, unique=True)),
                ('creation_date', models.CharField(max_length=100)),
                ('access_counter', models.IntegerField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='url_api.client')),
            ],
        ),
    ]
