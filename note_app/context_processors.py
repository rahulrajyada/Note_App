from .models import Note

def categories_list(request):
    # Return distinct categories in DB and map to display name if needed
    cats = list(Note.objects.values_list('category', flat=True).distinct())
    # Optional: map choice keys to human labels (if you used CATEGORY_CHOICES)
    labels = dict(Note.CATEGORY_CHOICES) if hasattr(Note, 'CATEGORY_CHOICES') else {}
    categories = [(c, labels.get(c, c.title())) for c in cats]
    # Sort by label
    categories.sort(key=lambda x: x[1])
    return {"navbar_categories": categories}
