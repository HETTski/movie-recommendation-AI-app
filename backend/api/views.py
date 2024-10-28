from django.shortcuts import render
#from django.contrib.auth.models import User
from .models import CustomUser, Movie
from rest_framework import generics, status
from .serializers import UserSerializer, MovieSerializer, AddMovieSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

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
        print(f"Request data: {request.data}")  # Dodaj to dla debugowania
        user = request.user
        movie_data = request.data

        serializer = AddMovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie_data = serializer.validated_data

        # Sprawdzenie, czy film o podanej nazwie już istnieje
        movie, created = Movie.objects.get_or_create(
            title=movie_data['title'],
            defaults={'description': movie_data.get('description', '')}
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