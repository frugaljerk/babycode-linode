from django.db import models

# Create your models here.
class NewsletterUser(models.Model):
    email = models.EmailField(unique=True, max_length=50)
    name = models.CharField(max_length=50)
    date_added = models.DateField(auto_now_add=True)
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email + " (" + ("not " if not self.confirmed else "") + "confirmed)"
