# Generated by Django 3.2.6 on 2021-09-27 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game_logs", "0013_auto_20210926_1646"),
    ]

    operations = [
        migrations.AddField(
            model_name="gamecharacter",
            name="orderimage_index",
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
