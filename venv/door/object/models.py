from django.db import models

# Create your models here.
class Object(models.Model):
    name = models.CharField(max_length=5000)
    image = models.ImageField(blank=True,null=True)
    entered = models.BooleanField(default=False)
    def __str__(self):
        type = 'enter'
        if not self.entered:
            type = 'exit'
        return self.name+' '+type

    class Meta :
        ordering = ['-id']
