from django.db import models

from .utils import create_item_choice

# Create your models here.


CHOICE = create_item_choice()


class TimeModel(models.Model):
    item = models.CharField(max_length=50, choices=CHOICE)
    memo = models.TextField(null=True, blank=True)
    starttime = models.DateTimeField(null=True, blank=True, default=None)
    endtime = models.DateTimeField(null=True, blank=True, default=None)
    duration = models.DurationField(null=True, blank=True)
    isactive = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return f"{self.get_item_display()}"

    def save(self, *args, **kwargs):
        try:
            self.duration = self.endtime - self.starttime
        except TypeError:  # 時間がNoneで保存された場合
            pass
        super().save(*args, **kwargs)
