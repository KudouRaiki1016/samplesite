# Generated by Django 4.1.2 on 2023-03-04 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]
