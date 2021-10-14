# Generated by Django 3.2.6 on 2021-10-04 00:29

from django.db import migrations, models
import game_logs.models


class Migration(migrations.Migration):

    dependencies = [
        ("game_logs", "0014_gamecharacter_orderimage_index"),
    ]

    operations = [
        migrations.AddField(
            model_name="gamedemo",
            name="originalgamefile",
            field=models.FileField(
                blank=True, upload_to=game_logs.models.GameDemo.game_directory_path
            ),
        ),
    ]
