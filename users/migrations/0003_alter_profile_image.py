# Generated by Django 3.2.6 on 2021-10-14 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_pics/default_profile_pic.png', upload_to='profile_pics'),
        ),
    ]
