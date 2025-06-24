from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.db.models import Q
from note_app.models import Note
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Note
from django.shortcuts import render, redirect

#for listing note
def note_list(request):
    category = request.GET.get('category')

    if category:
        notes = Note.objects.filter(category__iexact=category)
    else:
        notes = Note.objects.all()

    return render(request, 'note_list.html', {
        'notes': notes,
        'category': category,
    })



    
# for viewing note details
def note_detail(request, id):
    note = Note.objects.get(id=id)
    return render(
        request,
        "note_details.html",
        {"note" : note},
    )
    
# for createing note
def note_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        category = request.POST.get('category', '').strip()

        if not title or not content:
            return render(request, 'note_create.html', {
                'error': "Title and content are required.",
                'title': title,
                'content': content,
                'category': category,
            })

        Note.objects.create(title=title, content=content, category=category)
        return redirect('note_list')

    # On GET — show empty form
    return render(request, 'note_create.html')


    
    
#foe updating note

def note_update(request, id):
    note = Note.objects.get( id=id)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        category = request.POST.get('category', '').strip()

        if not title or not content:
            return render(request, 'note_create.html', {
                'note': note,
                'error': "Title and content are required.",
                'title': title,
                'content': content,
                'category': category,
            })

        note.title = title
        note.content = content
        note.category = category
        note.save()

        return redirect('note_detail', id=note.id)

    return render(request, 'note_create.html', {
        'note': note,
        'title': note.title,
        'content': note.content,
        'category': note.category
    })


    
#for deleting note
def note_delete(request,id):
    note = Note.objects.get(id=id)
    note.delete()
    return HttpResponseRedirect("/")



# for category
def notes_by_category(request, category):
    notes = Note.objects.filter(category__iexact=category)
    return render(request, "note_list.html", {
        "notes": notes,
        "category": category,
    })
    
# for searching

def note_search(request):
    query = request.GET.get('q', "").strip()

    if query:
        # Try exact title match (case-insensitive)
        try:
            note = Note.objects.get(title__iexact=query)
            return redirect('note_detail', id=note.id)
        except Note.DoesNotExist:
            # Fall back to partial search
            notes = Note.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(category__icontains=query)
            )
    else:
        notes = []

    return render(request, "note_search.html", {
        "notes": notes,
        "query": query,
    })









         
    