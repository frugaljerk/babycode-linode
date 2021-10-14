from django.db import models


class Contact(models.Model):
    contact_email = models.EmailField()
    contact_subject = models.CharField(max_length=255)
    contact_message = models.TextField()

    def __str__(self):
        return self.contact_email
