from django.shortcuts import render, redirect, get_object_or_404
from .forms import TagForm, NoteForm
from .models import Tag, Note


def main(request):
    notes = Note.objects.all()
    tags = Tag.objects.all()
    return render(request, 'notes/index.html', {"notes": notes, "tags":tags})


def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='notes:main')
        else:
            return render(request, 'notes/tag.html', {'form': form})

    return render(request, 'notes/tag.html', {'form': TagForm()})


def note(request):
    print(request.POST)
    tags = Tag.objects.all()
    try:
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)

            return redirect(to='notes:main')
        else:
            return render(request, 'notes/note.html', {"tags": tags, 'form': form})
    except:
        return render(request, 'notes/note.html', {"tags": tags, 'form': NoteForm()})


def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, 'notes/detail.html', {"note": note})


def delete_note(request, note_id):
    Note.objects.get(pk=note_id).delete()
    return redirect(to='notes:main')


def test(request):
    return render(request, "notes/test.html")
