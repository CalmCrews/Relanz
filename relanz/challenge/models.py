from django.db import models

# Create your models here.
class Challenge(models.Model):
    class Meta:
        db_table="challenge"

    title = models.CharField(max_length=32, unique=True, blank=False)
    sub_effect = models.TextField(blank=False)
    effect = models.TextField(blank=False)
    recommand = models.TextField(blank=False)
    image = models.ImageField()