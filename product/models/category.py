from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unique__(self):
        return self.title
    