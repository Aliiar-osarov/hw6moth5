from django.db import models

class Mixin(models.Model):
    title = models.CharField(max_length=123)
    description = models.TextField()
    created = models.DateField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Human(Mixin):
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    addres = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']
        
# DRY = Dont repeat yorself