from django.db import models


class CMSImageField(models.ImageField):
    def pre_save(self, model_instance, add):

        file = super(models.FileField, self).pre_save(model_instance, add)

        if file and not file._committed:
            # Commit the file to storage prior to saving the model
            file.save("%s.png" % model_instance.pk, file, save=False)
        return file
