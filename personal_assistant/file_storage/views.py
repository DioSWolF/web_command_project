from django.shortcuts import render, redirect, reverse
from .forms import MediaForm, ImageForm
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import File, Image
from django.http import HttpResponseRedirect



def upload_image(request):
    print(f"upload_image: {request.method}")

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        image = form.save(commit=False)
        image.owner = request.user
        image.save()
        return HttpResponseRedirect("/images/")
    return render(request, "file_storage/upload_image.html", {"form": ImageForm})



def upload_media(request):
    if request.method == "POST":
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save()
            media.owner = request.user
            media.save()
            print(f"primary key: {media.id}")
            # return HttpResponseRedirect('/upload_media/')
            return redirect(f"/file/{media.id}/")
        return HttpResponseRedirect("/upload_media/")

    return render(request, "file_storage/upload_media.html", {"form": MediaForm})



class FileDetailView(DetailView):
    print("detail view")
    model = File

class UserImagesListView(ListView):
    model = Image
    template_name = "file_storage/images"
    context_object_name = "images"


class UserFilesListView(ListView):
    model = File
    template_name = "file_storage/files"
    context_object_name = "files"



    def post(self, request, *args, **kwargs):
        file = self.get_object()
        if self.request.user == file.owner:
            if file.in_trash:
                file.in_trash = False
            else:
                file.in_trash = True
            file.save()
        return HttpResponseRedirect(f"/file/{file.id}/")


class FileUpdateView(UpdateView):
    model = File
    fields = [
        "name",
    ]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        file = self.get_object()
        if self.request.user == file.owner:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse('file-detail', args=[str(self.object.id)])


class FileDeleteView(DeleteView):
    model = File
    success_url = '/files/'

    def test_func(self):
        file = self.get_object()
        if self.request.user == file.owner:
            return True
        else:
            return False


class Folder:
    def __init__(self, name, datatype, image):
        self.name = name
        self.path_to_image = image
        self.datatype = datatype
        self.data = None


images = Folder("images", "image", "/media/images.png")
audio = Folder("audio", "audio", "/media/audio.png")
video = Folder("video", "video", "/media/video.png")
documents = Folder("documents", "document", "/media/documents.png")
other = Folder("other", "other", "/media/other.png")
trash = Folder("trash", None, "/media/trash.jpg")
folders = [images, audio, video, documents, other]


def file_list(request):
    user = request.user

    data = {"folders": []}
    for folder in folders:
        query = File.objects.filter(owner=user)\
            .filter(datatype=folder.datatype)\
            .filter(in_trash=False)\
            .order_by('name').all()
        folder.data = query
        data["folders"].append(folder)
    user_trash = trash
    query = File.objects.filter(owner=user)\
        .filter(in_trash=True)\
        .order_by('name').all()
    user_trash.data = query
    data["folders"].append(user_trash)

    recently_uploaded = []
    if request.method == "POST":
        print("posting")
        myfile = request.FILES.getlist("upload_files")
        for f in myfile:
            new_file = File(data=f, name=f._name, owner=user)
            new_file.save()
            recently_uploaded.append(new_file)
        # return redirect("/files/")
    data["uploaded"] = recently_uploaded
    return render(request, 'file_storage/file_list.html', data)


def image_list(request):
    user = request.user
    query = File.objects.filter(owner=user).filter(in_trash=False).filter(datatype="image").order_by('name').all()
    data = {
        'images': query,
    }
    print(data)
    return render(request, 'file_storage/image_list.html', data)


def video_list(request):
    user = request.user
    query = File.objects.filter(owner=user).filter(in_trash=False).filter(datatype="video").order_by('name').all()
    data = {
        'files': query,
    }
    print(data)
    return render(request, 'file_storage/video_list.html', data)


def audio_list(request):
    user = request.user
    query = File.objects.filter(owner=user).filter(in_trash=False).filter(datatype="audio").order_by('name').all()
    data = {
        'files': query,
    }
    print(data)
    return render(request, 'file_storage/audio_list.html', data)


def document_list(request):
    user = request.user
    query = File.objects.filter(owner=user).filter(in_trash=False).filter(datatype="document").order_by('name').all()
    data = {
        'files': query,
    }
    print(data)
    return render(request, 'file_storage/document_list.html', data)


def other_list(request):
    user = request.user
    query = File.objects.filter(owner=user).filter(in_trash=False).filter(datatype="other").order_by('name').all()
    data = {
        'files': query,
        'trash': False,
    }
    print(data)
    return render(request, 'file_storage/other_list.html', data)


def trash_list(request):
    user = request.user
    query = File.objects.filter(owner=user).filter(in_trash=True).order_by('name').all()
    data = {
        'files': query,
        'trash': True,
    }
    print(data)
    return render(request, 'file_storage/other_list.html', data)


def send_files(request):
    user = request.user
    print("uploading")
    if request.method == "POST":
        myfile = request.FILES.getlist("upload_files")
        for f in myfile:
            File(data=f, name=f._name, owner=user).save()
        return redirect("/files/")
    context = {
        "data": File.objects.all(),
    }
    return render(request, "file_storage/upload.html", context)

    