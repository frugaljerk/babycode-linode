from django.db import models


# Create your models here.
class GameDemo(models.Model):
    def game_directory_path(self, filename):
        return f"game_logs/game_{self.pk}/{filename}"

    """Main Game Demostration Videos accessible by Admin """
    title = models.CharField(max_length=100)
    description = models.TextField()
    link_to_video = models.URLField()
    display_image = models.ImageField(
        default="default_game_pic.png", upload_to=game_directory_path
    )
    date_added = models.DateTimeField(auto_now_add=True)
    gamefile = models.FileField(blank=True, upload_to=game_directory_path)
    originalgamefile = models.FileField(blank=True, upload_to=game_directory_path)

    example_image1 = models.ImageField(
        null=True, blank=True, upload_to=game_directory_path
    )  # use GIF
    example_image2 = models.ImageField(
        null=True, blank=True, upload_to=game_directory_path
    )
    example_image3 = models.ImageField(
        null=True, blank=True, upload_to=game_directory_path
    )
    example_image4 = models.ImageField(
        null=True, blank=True, upload_to=game_directory_path
    )

    number_of_characters = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["date_added"]

    def __str__(self):
        """Return a string representation of the model"""
        return self.title


class GameCharacter(models.Model):
    def directory_path(self, filename):
        return f"game_logs/characters/{filename}"

    name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to=directory_path)
    description = models.TextField()
    game = models.ForeignKey(GameDemo, on_delete=models.CASCADE)
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    orderimage_index = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.name


class CharacterPosture(models.Model):
    def directory_path(self, filename):
        return f"game_logs/postures/{filename}"

    name = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to=directory_path)
    character = models.ForeignKey(GameCharacter, on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.character}{self.name}"
