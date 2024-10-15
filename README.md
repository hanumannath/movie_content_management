# Movie Content Management System

This project implements a simple movie content management system for IMDb, allowing users to upload movie-related data via CSV files and retrieve it using pagination, filtering, and sorting features.

## Features

### 1. CSV Upload
- Allows the content team to upload movie-related data via a CSV file.
- File upload limit: 100 MB.

### 2. Movie List Retrieval
- Retrieve a paginated list of all movies.
- Filter options available: year of release, language.
- Sorting options available: release date, ratings.

## Technical Details

- **Tech Stack**: Django REST Framework
- **Database**: SQLite
- **Maximum CSV Size**: 100 MB

## API Endpoints

### 1. Upload Movies Data
- **Endpoint**: `/movies/upload_movies_data/`
- **Method**: `POST`
- **Description**: Uploads a CSV file containing movie data.
  
#### How to Upload CSV Data:
- Enter the URL of your endpoint (e.g., `http://localhost:8000/movies/upload_movies_data/`).
- In the "Body" tab (using tools like **Postman**), select `form-data`.
- Add a key named `csv_file`, and upload the CSV file containing movie data.

**Example in Postman:**
- URL: `http://localhost:8000/movies/upload_movies_data/`
- Method: `POST`
- Body: Select `form-data` and add the key `csv_file` with your file as the value.


### 2. Retrieve Movies List
- **Endpoint**: `/movies/movies/`
- **Method**: `GET`
- **Description**: Retrieves a paginated list of all movies with filtering and sorting options.
- **Query Parameters**:
    - `year_of_release`: Filter by release year (e.g., `http://localhost:8000/movies/movies/?year_of_release=1995`).
    - `language`: Filter by language (e.g., `http://localhost:8000/movies/movies/?language=English`).
    - `sort_by`: Sort by `release_date`, `rating`, or `vote_average` (e.g., `http://localhost:8000/movies/movies/?sort_by=release_date`).

### API Example Endpoints

- **Filter by Year**:  
  `http://localhost:8000/movies/movies/?year_of_release=1995`

- **Filter by Language**:  
  `http://localhost:8000/movies/movies/?language=English`

- **Sort by Release Date (Descending)**:  
  `http://localhost:8000/movies/movies/?sort_by=-release_date`

- **Sort by Ratings (Ascending)**:  
  `http://localhost:8000/movies/movies/?sort_by=rating`

- **Sort by Vote Average**:  
  `http://localhost:8000/movies/movies/?sort_by=vote_average`
