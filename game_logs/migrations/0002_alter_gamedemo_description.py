# Generated by Django 3.2.6 on 2021-08-30 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game_logs", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gamedemo",
            name="description",
            field=models.TextField(),
        ),
    ]
