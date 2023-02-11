from django.urls import path

from .views import upload_media, file_list, image_list, send_files, video_list, audio_list, document_list, other_list
from .views import trash_list
from .views import FileUpdateView, FileDetailView, FileDeleteView

urlpatterns = [
    path('upload_media/', upload_media),
    path('file/<int:pk>/',
         FileDetailView.as_view(),
         name='file-detail'),
    path('files/',
         file_list,
         name='data_storage-files'),
    path('images/', image_list, name='data_storage-images'),
    path('video/', video_list, name='data_storage-video'),
    path('audio/', audio_list, name='data_storage-audio'),
    path('documents/', document_list, name='data_storage-documents'),
    path('other/', other_list, name='data_storage-other'),
    path('trash/', trash_list, name='data_storage-trash'),
    path('upload/', send_files, name="uploads"),
    path('file/<int:pk>/update/', FileUpdateView.as_view(), name='file-update'),
    path('file/<int:pk>/delete/', FileDeleteView.as_view(), name='file-delete'),]

