# Generated by Django 4.1.2 on 2023-02-21 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("pzdrapp", "0002_awakening_remove_partypost_cloud_resistance_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partypost",
            name="awakenings",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="pzdrapp.awakening"
            ),
        ),
    ]
