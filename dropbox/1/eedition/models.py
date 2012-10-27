from django.db import models

class Edition(models.Model):
    date = models.DateField(unique=True)
    file = models.FileField(upload_to='pdf')
    def get_absolute_url(self):
        return self.date.strftime("/%Y/%m/%d")

class ScreenShot(models.Model):
    edition = models.ForeignKey(Edition)
    file = models.ImageField(upload_to='scr')