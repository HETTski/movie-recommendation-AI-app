from django.shortcuts import render
#from django.contrib.auth.models import User
from .models import CustomUser, Movie
from rest_framework import generics, status
from .serializers import UserSerializer, MovieSerializer, AddMovieSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from OpenAI.main import get_movie_recommendations, chatbot_conversation

# Create your views here.
class CreateUserView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.raw('SELECT * FROM users')
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserMoviesView(generics.ListAPIView):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print(f"User: {user.username}")  # Sprawdź, kto jest zalogowany
        print(f"User.movies: {user.movies}")  # Sprawdź, kto jest zalogowany
        movie_ids = user.movies

        if movie_ids:
            return Movie.objects.filter(id__in=movie_ids)
        else:
            return Movie.objects.none()  # Zwróć pusty queryset, jeśli nie ma filmów

class AddUserMovieView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        movie_data = request.data

        serializer = AddMovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie_data = serializer.validated_data

        # Sprawdzenie, czy film o podanej nazwie już istnieje
        movie, created = Movie.objects.get_or_create(
            title=movie_data['title'],
            defaults={
                'description': movie_data.get('description', ''),
                'sites': movie_data.get('sites', [])
            }
        )

        # Dodanie ID filmu do pola `movies` użytkownika, jeśli go tam jeszcze nie ma
        if movie.id not in user.movies:
            user.movies.append(movie.id)
            user.save()

        return Response(
            {
                'message': 'Film został dodany do listy użytkownika.',
                'movie': MovieSerializer(movie).data,
                'user_movies': user.movies
            },
            status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED
        )

class RecommendationView(APIView):
    permission_classes = [AllowAny]  # Allow all users, anonymous or authenticated

    def post(self, request):
        genres = request.data.get("genres", [])
        
        if request.user.is_authenticated:
            watched_movies = request.user.movies  # List of movie IDs the user has watched
            recommendations = get_movie_recommendations(genres=genres, exclude_ids=watched_movies)
        else:
            recommendations = get_movie_recommendations(genres=genres)
        
        return Response(
            {"recommendations": recommendations},
            status=status.HTTP_200_OK
        )

class MovieRecommendationView(APIView):
    permission_classes = [AllowAny]  # Allow all users, anonymous or authenticated

    def post(self, request):
        if request.user.is_authenticated:
            movie_ids = request.user.movies
            if movie_ids:
                watched_movies = []  # List of movie IDs the user has watched
                moviesArray = Movie.objects.filter(id__in=movie_ids)
                for m in moviesArray:
                    watched_movies.append(m.title)
        else:
            watched_movies = request.data.get('watched_movies', [])
        query = request.data.get('query', "Can you recommend a movie for me?")
        
        # Build the initial conversation context
        conversation_context = f"Based on the movies {watched_movies}, recommend some similar movies. {query}"
        
        # Call the conversational function instead
        response = chatbot_conversation(conversation_context)
        
        return Response({"recommendations": response}, status=200)
   