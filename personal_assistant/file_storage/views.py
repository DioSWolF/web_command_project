from django.shortcuts import render, reverse

from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import File, ProfileData

from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .forms import FilterForm
from django.contrib import messages
from .src import stat_plot


class FilterUpdateView(UpdateView):
    model = ProfileData
    fields = ["filter", "reversed_sort"]


    def get_success_url(self):
        return reverse('data_storage-files')


class FileDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = File
    # print(self.request.user)

    def post(self, request, *args, **kwargs):
        file = self.get_object()
        if self.request.user == file.owner:
            if file.in_trash:
                file.in_trash = False
            else:
                file.in_trash = True
            file.save()
        return HttpResponseRedirect(f"/file/{file.id}/")

    def test_func(self):
        file = self.get_object()
        if self.request.user == file.owner:
            return True
        else:
            return False


class UserFilesListView(LoginRequiredMixin, ListView):
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


class FileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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


class FileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
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


@login_required(login_url='/login/')
def file_list(request):

    user = request.user
    memory_chart = None
    filter_inst = ProfileData.objects.filter(user=user).all()
    if len(filter_inst) != 1:
        new_filter = ProfileData(user=user)
        new_filter.save()
        return HttpResponseRedirect('/files/')
    else:
        filter_inst[0].memory_occupied = 0
        query = File.objects.filter(owner=user).all()
        memory_chart = stat_plot.get_plot(query, user)
        filter_inst[0].num_of_files = len(query)
        for file in query:
            filter_inst[0].memory_occupied += file.size
        filter_inst[0].save()

    data = {"folders": []}
    data["memory_chart"] = memory_chart
    recently_uploaded = []

    for folder in folders:
        query = File.objects.filter(owner=user).filter(datatype=folder.datatype).filter(in_trash=False)\
            .order_by('name').all()
        folder.data = query
        folder.num_of_files = len(query)
        data["folders"].append(folder)
    user_trash = trash
    query = File.objects.filter(owner=user)\
        .filter(in_trash=True)\
        .order_by('name').all()

    user_trash.data = query
    user_trash.num_of_files = len(query)
    data["folders"].append(user_trash)

    if request.method == "POST":
        filter_form = FilterForm(request.POST)
        if filter_form.is_valid():
            filter_by = filter_form.cleaned_data.get("filter_by")
            reversed_sort = filter_form.cleaned_data.get("reversed_sort")
            if len(filter_inst) != 1:
                new_filter = ProfileData(user=user, filter_by=filter_by, reversed_sort=reversed_sort)
                new_filter.save()
            else:
                filter_inst[0].filter_by = filter_by
                filter_inst[0].reversed_sort = reversed_sort
                filter_inst[0].save()

        myfile = request.FILES.getlist("upload_files")
        for f in myfile:
            if filter_inst[0].max_capacity < filter_inst[0].memory_occupied + f.size:
                messages.error(request,
                               f'UPLOAD ERROR: Memory limit exceeded '
                               f'({filter_inst[0].max_capacity // 1024 //1024} MB)')
                break
            if filter_inst[0].num_of_files + 1 > filter_inst[0].max_num_of_files:
                messages.error(request, f'UPLOAD ERROR: Number of files limit exceed '
                                        f'({filter_inst[0].max_num_of_files} files)')
                break
            else:
                new_file = File(data=f, name=f._name, owner=user, size=f.size)
                filter_inst[0].memory_occupied += f.size
                filter_inst[0].num_of_files += 1
                new_file.save()
                filter_inst[0].save()
                messages.success(request, f'{new_file.name} has been successfully uploaded')
                recently_uploaded.append(new_file)

        data["uploaded"] = recently_uploaded
        # return render(request, 'file_storage/file_list.html', data)
        return HttpResponseRedirect('/files/')

    if len(filter_inst) != 1:
        filter_form = FilterForm(initial={'filter_by': 'date_posted', 'reversed_sort': False})
    else:
        filter_form = FilterForm(initial={'filter_by': filter_inst[0].filter_by,
                                          'reversed_sort': filter_inst[0].reversed_sort})

    filter_form.fields['filter_by'].initial = filter_inst[0].filter_by
    data["filter_form"] = filter_form

    # add files
    query = File.objects.filter(owner=user).filter(in_trash=False)\
        .order_by('name').order_by(f'{filter_inst[0].filter_by}').all()
    if filter_inst[0].reversed_sort:
        query = query.reverse()
    data["files"] = query

    return render(request, 'file_storage/file_list.html', data)


def media_list(data_type="", template="", data_types="", in_trash=False):
    def iner(request):
        user = request.user
        data = {}
        filter_inst = ProfileData.objects.filter(user=user).all()
        if request.method == "POST":
            filter_form = FilterForm(request.POST)
            if filter_form.is_valid():
                filter_by = filter_form.cleaned_data.get("filter_by")
                reversed_sort = filter_form.cleaned_data.get("reversed_sort")
                if len(filter_inst) != 1:
                    new_filter = ProfileData(user=user, filter_by=filter_by, reversed_sort=reversed_sort)
                    new_filter.save()
                else:
                    filter_inst[0].filter_by = filter_by
                    filter_inst[0].reversed_sort = reversed_sort
                    filter_inst[0].save()
            return HttpResponseRedirect(f'/{data_types}/')

        if len(filter_inst) != 1:
            filter_form = FilterForm(initial={'filter_by': 'date_posted', 'reversed_sort': False})
        else:
            filter_form = FilterForm(initial={'filter_by': filter_inst[0].filter_by,
                                              'reversed_sort': filter_inst[0].reversed_sort})
        filter_form.fields['filter_by'].initial = filter_inst[0].filter_by
        data["filter_form"] = filter_form

        if data_type:
            query = File.objects.filter(owner=user).\
                filter(in_trash=in_trash).\
                filter(datatype=data_type).\
                order_by(f'{filter_inst[0].filter_by}').all()
        else:
            query = File.objects.filter(owner=user). \
                filter(in_trash=in_trash). \
                order_by(f'{filter_inst[0].filter_by}').all()
        if filter_inst[0].reversed_sort:
            query = query.reverse()
        data["files"] = query
        if in_trash:
            data["trash"] = True
        return render(request, f'file_storage/{template}/', data)
    return iner


@login_required(login_url='/login/')
def video_list(request):
    return media_list(data_type="video", template="video_list.html", data_types="video")(request)


@login_required(login_url='/login/')
def audio_list(request):
    return media_list(data_type="audio", template="audio_list.html", data_types="audio")(request)


@login_required(login_url='/login/')
def image_list(request):
    return media_list(data_type="image", template="image_list.html", data_types="images")(request)


@login_required(login_url='/login/')
def document_list(request):
    return media_list(data_type="document", template="document_list.html", data_types="documents")(request)


@login_required(login_url='/login/')
def other_list(request):
    return media_list(data_type="other", template="other_list.html", data_types="other")(request)


@login_required(login_url='/login/')
def trash_list(request):
    return media_list(data_type="", template="other_list.html", data_types="other", in_trash=True)(request)


