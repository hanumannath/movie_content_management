from django.contrib import admin
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'original_title', 'release_date', 'vote_average', 'original_language', 'languages')

admin.site.register(Movie, MovieAdmin)
