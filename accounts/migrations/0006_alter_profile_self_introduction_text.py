# Generated by Django 4.1.2 on 2023-03-22 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_profile_self_introduction_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="self_introduction_text",
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
