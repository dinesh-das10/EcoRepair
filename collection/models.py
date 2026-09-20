from django.db import models


class CollectionCenter(models.Model):
    CATEGORY_CHOICES = [
        ('mobile', 'Mobile'),
        ('mixer', 'Mixer/Grinder'),
        ('washing_machine', 'Washing Machine'),
        ('laptop', 'Laptop'),
        ('fan', 'Fan'),
        ('refrigerator', 'Refrigerator'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    accepted_categories = models.JSONField(default=list)
    operating_info = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name