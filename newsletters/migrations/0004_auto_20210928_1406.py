# Generated by Django 3.2.6 on 2021-09-28 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("newsletters", "0003_auto_20210928_1035"),
    ]

    operations = [
        migrations.AddField(
            model_name="newsletteruser",
            name="conf_num",
            field=models.CharField(default=123, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="newsletteruser",
            name="confirmed",
            field=models.BooleanField(default=False),
        ),
    ]
