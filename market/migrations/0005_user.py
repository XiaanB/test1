# Generated by Django 5.1 on 2024-09-01 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0004_pricehistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=30, unique=True)),
                ('user_password', models.CharField(max_length=30)),
                ('user_email', models.EmailField(max_length=254)),
                ('user_type', models.CharField(max_length=30)),
            ],
        ),
    ]