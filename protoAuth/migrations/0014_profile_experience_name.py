# Generated by Django 5.0 on 2024-03-02 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protoAuth', '0013_profile_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='experience_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
