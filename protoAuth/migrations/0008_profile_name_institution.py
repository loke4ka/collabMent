# Generated by Django 5.0 on 2024-03-01 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protoAuth', '0007_profile_education_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name_institution',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
