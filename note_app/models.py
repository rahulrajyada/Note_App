
from django.db import models
from django.conf import settings

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
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notes",
        help_text="User who created this note"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
