import csv

from django.db.models import Q
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieSerializer


class MovieUploadView(APIView):
    """
    API View to handle CSV file uploads for movie records.

    Accepts a CSV file containing movie data and creates movie records in bulk.
    Returns success or error messages based on the operation results.
    """
    # limiting the size of uploaded file to be less than 100MB
    FILE_SIZE_LIMIT = 100 * 1024 * 1024

    def post(self, request):
        """
        Handles POST requests for uploading a CSV file.

        Validates the uploaded file, processes the CSV content, and creates
        movie records. Returns a response indicating success or errors.

        Parameters:
        - request: The HTTP request containing the CSV file.

        Returns:
        - Response: A Response object with status and messages.
        """
        csv_file = request.FILES.get('csv_file')

        if csv_file.size > self.FILE_SIZE_LIMIT:
            return Response(
                {'error': 'File size exceeds the limit of 100 MB.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not csv_file:
            return Response({'error': 'Please upload a CSV file.'}, status=status.HTTP_400_BAD_REQUEST)

        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'Uploaded file is not a CSV file.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            movies_to_create = []
            errors = []

            for index, row in enumerate(reader):
                serializer = MovieSerializer(data=row)
                if serializer.is_valid():
                    movies_to_create.append(serializer.validated_data)
                else:
                    errors.append(f"Row {index + 1}: {serializer.errors}")

            if movies_to_create:
                Movie.objects.bulk_create([Movie(**movie) for movie in movies_to_create])

            response = {
                'status': 'success',
                'movies_created': len(movies_to_create),
                'errors': errors
            }

            return Response(response, status=status.HTTP_201_CREATED)

        except csv.Error as e:
            return Response({'error': f'CSV parsing error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MoviePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class MovieListView(APIView):
    """
    A view that returns a list of movies with optional filtering and sorting.

    Query Parameters:
    - `year_of_release`: (optional) Filter movies by release year.
    - `language`: (optional) Filter movies by original language or available languages (case-insensitive).
    - `sort_by`: (optional) Sort movies by either release date or vote average.
      Acceptable values are 'release_date', '-release_date', 'vote_average', '-vote_average'.

    Returns:
    - A paginated response containing a list of movies that match the applied filters and sorting criteria.
    """

    queryset = Movie.objects.all()
    pagination_class = MoviePagination

    def get(self, request):
        movies = self.queryset

        release_year = request.query_params.get('year_of_release', None)
        language = request.query_params.get('language', None)

        if release_year:
            movies = movies.filter(release_date__year=release_year)

        # We check case-insensitively if the language exists in the original language or languages
        if language:
            movies = movies.filter(
                Q(original_language__icontains=language) |
                Q(languages__icontains=language)
            )

        # Sort if any parameter is provided for sorting
        sort_by = request.query_params.get('sort_by', None)
        if sort_by:
            if sort_by in ['release_date', '-release_date', 'vote_average', '-vote_average']:
                movies = movies.order_by(sort_by)

        # Pagination
        paginator = MoviePagination()
        paginated_movies = paginator.paginate_queryset(movies, request)

        serializer = MovieSerializer(paginated_movies, many=True)

        return paginator.get_paginated_response(serializer.data)
