from django.db import models

class Note(models.Model):
    CATEGORY_CHOICES = [
        ("work", "Work"),
        ("personal", "Personal"),
        ("study", "Study"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=256)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="other")

    def __str__(self):
        return self.title

  
