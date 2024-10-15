from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200, blank=True)
    overview = models.TextField(blank=True)
    release_date = models.DateField()
    revenue = models.FloatField(default=0)
    budget = models.FloatField(default=0)
    runtime = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50)
    vote_average = models.FloatField(default=0)
    vote_count = models.PositiveIntegerField(default=0)
    original_language = models.CharField(max_length=50)
    production_company_id = models.PositiveIntegerField()
    genre_id = models.PositiveIntegerField()
    languages = models.TextField(blank=True)
    homepage = models.URLField(blank=True)

    def __str__(self):
        return self.title
