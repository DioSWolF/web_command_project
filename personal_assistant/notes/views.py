from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TagForm, NoteForm
from .models import Tag, Note


@login_required(login_url='/login/')
def main(request):
    notes = Note.objects.all().filter(owner=request.user)
    tags = Tag.objects.all().filter(owner=request.user)
    if request.method == "POST":
        question = request.POST.get("question")
        if not question.strip() == '':
            by_tags = list()
            by_desc = list()
            by_name = list()
            for each in notes:
                note_tags = list()
                for tag in each.tags.all():
                    note_tags.append(tag.name)
                if question in each.description:
                    by_desc.append(each)
                if question in note_tags:
                    by_tags.append(each)
                if question in each.name:
                    by_name.append(each)
            if len(by_name) > 0 or len(by_tags) > 0 or len(by_desc) > 0:
                by_tags.insert(0, "BLANKTAG")
            return render(request, 'notes/index.html', {"by_tags": by_tags, "by_desc": by_desc, "by_name": by_name})
    return render(request, 'notes/index.html', {"notes": notes, "tags": tags})


@login_required(login_url='/login/')
def tag(request):
    if request.method == 'POST':
        names = request.POST.get("name").split(",")
        request.POST = request.POST.copy()
        for each in names:
            each.strip()
            if not each.startswith("#"):
                each = "#" + each.strip()
            request.POST.update({"name": each})
            form = TagForm({"owner": request.user, "name": request.POST.get('name')})
            if form.is_valid():
                form.save()
        return redirect(to='notes:main')

    return render(request, 'notes/tag.html', {'form': TagForm()})


@login_required(login_url='/login/')
def note(request):
    tags = Tag.objects.all().filter(owner=request.user)
    try:
        form = NoteForm(
            {"name": request.POST.get('name'), "description": request.POST.get("description"), "owner": request.user})
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


@login_required(login_url='/login/')
def delete_note(request, note_id):
    Note.objects.get(pk=note_id, owner=request.user).delete()
    return redirect(to='notes:main')


@login_required(login_url='/login/')
def edit(request, note_id):
    tags = Tag.objects.all().filter(owner=request.user)
    note = get_object_or_404(Note, pk=note_id, owner=request.user)
    if note:
        return render(request, 'notes/edit.html', {"note": note, "tags": tags})
    else:
        return redirect(to="notes:main")


@login_required(login_url='/login/')
def alteration(request, note_id, action):
    note = get_object_or_404(Note, pk=note_id, owner=request.user)
    match action:
        case 'Δ':
            note.description = request.POST.get('description')
            note.save()
            return redirect("notes:edit", note_id=note_id)
        case '+':
            for each in note.tags.all():
                note.tags.remove(each)
            print(request.POST.getlist('tags'))
            for each in request.POST.getlist('tags'):
                tag = get_object_or_404(Tag, name=each)
                note.tags.add(tag)
            return redirect("notes:edit", note_id=note_id)
