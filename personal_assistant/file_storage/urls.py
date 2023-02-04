from django.urls import path
from .views import upload_image, upload_media, file_list
from .views import UserImagesListView, ImageDetailedView, UserFilesListView, FileUpdateView

urlpatterns = [
    path('upload_image/', upload_image),
    path('upload_media/', upload_media),

    path('images/',
         UserImagesListView.as_view(),
         name='data_storage-images'),
    path('file/<int:pk>/',
         FileUpdateView.as_view(),
         name='file-detail'),
    path('files/',
         file_list,
         name='data_storage-files'),
    path('image/<int:pk>/',
         ImageDetailedView.as_view(),
         name='image-detail'),
]
