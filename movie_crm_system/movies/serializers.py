from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    release_date = serializers.DateField(required=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def validate_release_date(self, value):
        if not value:
            raise serializers.ValidationError("Invalid or missing release date.")
        return value
