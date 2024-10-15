from django.urls import path
from .views import MovieUploadView, MovieListView

urlpatterns = [
    path('upload_movies_data/', MovieUploadView.as_view()),
    path('movies/', MovieListView.as_view()),
]
