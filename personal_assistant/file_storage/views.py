from django.shortcuts import render, redirect
from .forms import ImageForm, MediaForm
from django.views.generic import ListView, DetailView, UpdateView
from .models import Image, File
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


class UserImagesListView(ListView):
    model = Image
    template_name = "file_storage/images"
    context_object_name = "images"


class UserFilesListView(ListView):
    model = File
    template_name = "file_storage/files"
    context_object_name = "files"


class ImageDetailedView(DetailView):
    model = Image
    # template_name = 'file_storage/image_detail.html'
    # context_object_name = 'images'


class FileUpdateView(UpdateView):
    model = File
    fields = [
        "name",
    ]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        transaction = self.get_object()
        if self.request.user == transaction.owner:
            return True
        else:
            return False


def file_list(request):
    user = request.user
    query_images = (
        File.objects.filter(owner=user).filter(datatype="image").order_by("name").all()
    )
    query_videos = (
        File.objects.filter(owner=user).filter(datatype="video").order_by("name").all()
    )
    query_audios = (
        File.objects.filter(owner=user).filter(datatype="audio").order_by("name").all()
    )
    query_documents = (
        File.objects.filter(owner=user)
        .filter(datatype="document")
        .order_by("name")
        .all()
    )
    query_other = (
        File.objects.filter(owner=user).filter(datatype="other").order_by("name").all()
    )
    data = {
        "images": query_images,
        "documents": query_documents,
        "audio": query_audios,
        "video": query_videos,
        "other": query_other,
    }
    return render(request, "file_storage/file_list.html", data)
