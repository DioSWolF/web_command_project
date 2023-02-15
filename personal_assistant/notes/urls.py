from django.urls import path

from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/', views.tag, name='tag'),
    path('note/', views.note, name='note'),
    path('delete/<int:note_id>', views.delete_note, name='delete'),
    path('edit/<int:note_id>', views.edit, name='edit'),
    path('alteration/<int:note_id>/<str:action>', views.alteration, name='alteration'),
]