from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="profile_pics\default_profile_pic.png", upload_to="profile_pics"
    )

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(
        self, *args, **kwargs
    ):  # override the existing save method to control image size
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


# Signal to delete order directory from hard drive.
@receiver(post_delete, sender=Profile)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.image.delete(False)