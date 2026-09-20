from django.db import models


class FaultPattern(models.Model):
    CATEGORY_CHOICES = [
        ('mobile', 'Mobile'),
        ('mixer', 'Mixer/Grinder'),
        ('washing_machine', 'Washing Machine'),
        ('laptop', 'Laptop'),
        ('fan', 'Fan'),
        ('refrigerator', 'Refrigerator'),
        ('other', 'Other'),
    ]

    VERDICT_CHOICES = [
        ('repairable', 'Repairable'),
        ('uncertain', 'Uncertain'),
        ('not_economical', 'Not Economical'),
    ]

    DIFFICULTY_CHOICES = [
        ('diy', 'DIY-Friendly'),
        ('professional', 'Professional Required'),
    ]

    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    symptom = models.TextField()
    verdict = models.CharField(max_length=20, choices=VERDICT_CHOICES)
    reason = models.TextField()
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        blank=True
    )
    repair_guide = models.TextField(blank=True)

    def __str__(self):
        return f"{self.category} - {self.symptom[:50]}"