# Generated by Django 4.1.2 on 2023-02-22 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pzdrapp", "0004_folder"),
    ]

    operations = [
        migrations.AddField(
            model_name="folder",
            name="thumbnail",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]
