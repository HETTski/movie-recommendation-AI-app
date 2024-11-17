from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.postgres.fields import ArrayField

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Haszowanie hasła
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = ''
    movies = ArrayField(models.IntegerField(), default=list, blank=True)
    #movies = models.ManyToManyField('Movie', related_name='users', blank=True)
    last_login = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # Żadne inne pola nie są wymagane przy tworzeniu użytkownika

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'  # Ustal nazwę tabeli

    def __str__(self):
        return self.username

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    sites = ArrayField(models.URLField(), blank=True, default=list)

    class Meta:
        db_table = 'movies'  # Ustaw nazwę tabeli na 'movies'

    def __str__(self):
        return self.title
