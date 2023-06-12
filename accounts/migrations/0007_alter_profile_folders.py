# Generated by Django 4.1.2 on 2023-04-01 03:29

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_alter_profile_self_introduction_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="folders",
            field=django_mysql.models.ListTextField(
                models.IntegerField(), blank=True, null=True, size=100
            ),
        ),
    ]
