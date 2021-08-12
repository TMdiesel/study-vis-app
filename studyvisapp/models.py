from django.db import models

# Create your models here.


CHOICE = (("danger", "機械学習"), ("warning", "統計"), ("primary", "読書"))


class TimeModel(models.Model):
    item = models.CharField(max_length=50, choices=CHOICE)
    memo = models.TextField(null=True, blank=True)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    duration = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_item_display()}"

    def save(self, *args, **kwargs):
        self.duration = self.endtime - self.starttime
        super().save(*args, **kwargs)
