# Generated by Django 3.2.6 on 2021-09-03 22:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("game_logs", "0003_alter_gamedemo_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gamedemo",
            name="image",
            field=models.ImageField(
                default="default_game_pic.png", upload_to="game_logs"
            ),
        ),
        migrations.CreateModel(
            name="MyBabyCodes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.BooleanField(default=False)),
                ("data_added", models.DateField(auto_now_add=True)),
                (
                    "image1",
                    models.ImageField(
                        default="default_game_pic.png", upload_to="order_pics"
                    ),
                ),
                (
                    "image2",
                    models.ImageField(
                        default="default_game_pic.png", upload_to="order_pics"
                    ),
                ),
                (
                    "image3",
                    models.ImageField(
                        default="default_game_pic.png", upload_to="order_pics"
                    ),
                ),
                (
                    "image4",
                    models.ImageField(
                        default="default_game_pic.png", upload_to="order_pics"
                    ),
                ),
                (
                    "image5",
                    models.ImageField(
                        default="default_game_pic.png", upload_to="order_pics"
                    ),
                ),
                (
                    "image6",
                    models.ImageField(
                        default="default_game_pic.png", upload_to="order_pics"
                    ),
                ),
                (
                    "image7",
                    models.ImageField(
                        default="default_game_pic.png", upload_to="order_pics"
                    ),
                ),
                (
                    "image8",
                    models.ImageField(
                        default="default_game_pic.png", upload_to="order_pics"
                    ),
                ),
                (
                    "image9",
                    models.ImageField(
                        default="default_game_pic.png", upload_to="order_pics"
                    ),
                ),
                (
                    "image10",
                    models.ImageField(
                        default="default_game_pic.png", upload_to="order_pics"
                    ),
                ),
                (
                    "game_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="game_logs.gamedemo",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
