from django.contrib.auth.models import User
from game_logs.models import GameDemo
from django.db import models
import uuid
import re, os, shutil
from babycode import settings
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver

# Model to store preprocessed images/games
class MyBabyCodes(models.Model):
    # counter to number image files
    counter = 1
    # Set up image storage destination folder with unique id
    def upload_path(self, filename):
        # assign unique order id to image folder

        if not self.pk:
            global i
            i = str(uuid.uuid4())[:8]
            self.id = self.pk = i

        # Rename imagefiles in numerical format (ie image1, image2, image3)
        regex = "\.(?i)(jpe?g|png|gif|bmp)$"
        file_extension = re.search(regex, filename).group()
        filename = "image" + str(self.counter) + file_extension
        self.counter += 1
        return f"order_pics/order_{str(self.order_id)}/{filename}"

    """To record users's game orders"""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    game_id = models.ForeignKey(GameDemo, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20, primary_key=True)
    # status = models.BooleanField(default=False)  # True for Order complete, False for Order in progress(use later on for animated games)
    date_added = models.DateTimeField(editable=True, auto_now_add=True)
    image1 = models.ImageField(
        upload_to=upload_path, blank=True
    )  # filename format userId_gameId_image#
    image2 = models.ImageField(upload_to=upload_path, blank=True)
    image3 = models.ImageField(upload_to=upload_path, blank=True)
    image4 = models.ImageField(upload_to=upload_path, blank=True)
    image5 = models.ImageField(upload_to=upload_path, blank=True)
    image6 = models.ImageField(upload_to=upload_path, blank=True)
    image7 = models.ImageField(upload_to=upload_path, blank=True)
    image8 = models.ImageField(upload_to=upload_path, blank=True)
    image9 = models.ImageField(upload_to=upload_path, blank=True)
    image10 = models.ImageField(upload_to=upload_path, blank=True)

    gamefile = models.FileField(blank=True)

    def __str__(self):
        """Return a string representation of the model by id"""
        return f"order id: {self.order_id}"  # primary order_id of the model


# Sign to delete order directory from hard drive.
@receiver(post_delete, sender=MyBabyCodes)
def mymodel_delete(sender, instance, **kwargs):

    path_to_folder = os.path.join(settings.MEDIA_ROOT, 'order_pics', rf'order_{instance.order_id}').replace("\\", '/')
    try:
        shutil.rmtree(path_to_folder)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
