from django.urls import path
from note_app import views

urlpatterns = [
    path("", views.note_list, name="note_list"),
    path('note/<int:id>/', views.note_detail, name='note_detail'),
    path("create/", views.note_create, name="note_create"),
    path("note_update/<int:id>/", views.note_update, name="note_update"),
    path("delete/<int:id>", views.note_delete, name="note_delete"),
    path('search/', views.note_search, name='note_search'),
    path("category/<str:category>/", views.notes_by_category, name="notes_by_category"),    
]
