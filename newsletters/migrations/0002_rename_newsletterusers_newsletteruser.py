# Generated by Django 3.2.6 on 2021-09-28 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("newsletters", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="NewsletterUsers",
            new_name="NewsletterUser",
        ),
    ]
