
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse
from .models import Note

def note_list(request):
    """Public: list notes, optionally filter by category"""
    category = request.GET.get('category')
    if category:
        notes = Note.objects.filter(category__iexact=category).order_by('-created_at')
    else:
        notes = Note.objects.all().order_by('-created_at')
    return render(request, "note_list.html", {"notes": notes, "category": category})

def note_detail(request, id):
    """Public: show note detail"""
    note = get_object_or_404(Note, id=id)
    return render(request, "note_details.html", {"note": note})

@login_required
def note_create(request):
    """Create a new note — only for logged-in users"""
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        category = request.POST.get("category", "other").strip()

        if not title or not content:
            return render(request, "note_create.html", {
                "error": "Title and content are required.",
                "title": title,
                "content": content,
                "category": category,
            })

        note = Note.objects.create(
            title=title,
            content=content,
            category=category,
            owner=request.user
        )
        return redirect("note_detail", id=note.id)

    # GET
    return render(request, "note_create.html", {
    "title": "",
    "content": "",
    "category": "other",
    "note": None,
      })


@login_required
def note_update(request, id):
    """Edit a note — only owner or staff allowed"""
    note = get_object_or_404(Note, id=id)

    # Permission check
    if note.owner is not None and note.owner != request.user and not request.user.is_staff:
        return render(request, "error.html", {"message": "You do not have permission to edit this note."})

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        category = request.POST.get("category", "other").strip()

        if not title or not content:
            return render(request, "note_create.html", {
                "error": "Title and content are required.",
                "note": note,
                "title": title,
                "content": content,
                "category": category,
            })

        note.title = title
        note.content = content
        note.category = category
        note.save()
        return redirect("note_detail", id=note.id)

    # GET
    return render(request, "note_create.html", {"note": note})

@login_required
def note_delete(request, id):
    """Delete a note — only owner or staff allowed"""
    note = get_object_or_404(Note, id=id)

    # Permission check
    if note.owner is not None and note.owner != request.user and not request.user.is_staff:
        return render(request, "error.html", {"message": "You do not have permission to delete this note."})

    if request.method == "POST":
        # Confirmed deletion
        note.delete()
        return redirect("note_list")

    # GET: ask for confirmation
    return render(request, "note_confirm_delete.html", {"note": note})

def notes_by_category(request, category):
    notes = Note.objects.filter(category__iexact=category).order_by('-created_at')
    return render(request, "note_list.html", {"notes": notes, "category": category})

def note_search(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return redirect("note_list")

    # Try exact title match first, else fallback to partial matches
    try:
        note = Note.objects.get(title__iexact=query)
        return redirect("note_detail", id=note.id)
    except Note.DoesNotExist:
        notes = Note.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(category__icontains=query)
        ).order_by('-created_at')
        return render(request, "note_search.html", {"notes": notes, "query": query})
