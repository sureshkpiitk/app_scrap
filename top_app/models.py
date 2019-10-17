import os
from urllib import request

from django.core.files import File
from django.db import models

# Create your models here.


class App(models.Model):
    package_name = models.CharField(max_length=250, null=True, blank=True, db_index=True, unique=True)
    name = models.CharField(max_length=250)
    icon = models.ImageField(null=True, blank=True)
    is_top = models.BooleanField(default=True)
    developer = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        app_label = 'top_app'

    def get_remote_image(self, url):
        if url and not self.icon:
            result = request.urlretrieve(url)
            self.icon.save(
                os.path.basename(f'{self.package_name}.jpg'),
                File(open(result[0], 'rb'))
            )
            self.save()


class ScreenShot(models.Model):
    app = models.ForeignKey(App, related_name='screen_shot', db_index=True, on_delete=models.CASCADE)
    url = models.URLField(null=True, blank=True)

    class Meta:
        app_label = 'top_app'
        unique_together = ['app', 'url']


class Video(models.Model):
    app = models.ForeignKey(App, related_name='videos', db_index=True, on_delete=models.CASCADE)
    url = models.URLField(null=True, blank=True)
    thumbnail = models.URLField(null=True, blank=True)

    class Meta:
        app_label = 'top_app'
        unique_together = ['app', 'url']
