# Generated by Django 3.2.6 on 2021-09-28 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("newsletters", "0002_rename_newsletterusers_newsletteruser"),
    ]

    operations = [
        migrations.AddField(
            model_name="newsletteruser",
            name="name",
            field=models.CharField(default="Fred Chiang", max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="newsletteruser",
            name="email",
            field=models.EmailField(max_length=50, unique=True),
        ),
    ]
