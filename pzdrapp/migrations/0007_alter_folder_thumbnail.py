# Generated by Django 4.1.2 on 2023-02-27 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pzdrapp", "0006_alter_partypost_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="folder",
            name="thumbnail",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]
