from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    dark_background = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["email"]


class Game(models.Model):
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('rpg', 'RPG'),
        ('strategy', 'Strategy'),
        ('adventure', 'Adventure'),
        ('survival', 'Survival'),
        ('sandbox', 'Sandbox'),
        ('shooter', 'Shooter'),
        ('simulation', 'Simulation'),
        ('horror', 'Horror'),
        ('sport', 'Sport'),
        ('racing', 'Racing'),
        ('indie', 'Indie'),
    ]

    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    avg_rating = models.FloatField(default=0)
    image = models.ImageField(upload_to='games/')
    description = models.TextField()

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    games = models.ManyToManyField(Game, blank=True)

    def total_price(self):
        return sum(game.price for game in self.games.all())


class Library(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='library'
    )


class LibraryGame(models.Model):
    STATUS_CHOICES = [
        ('playing', 'Граю'),
        ('completed', 'Пройшов'),
        ('wishlist', 'Хочу пройти'),
    ]

    library = models.ForeignKey(
        Library,
        on_delete=models.CASCADE,
        related_name='library_games'
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='wishlist'
    )

    class Meta:
        unique_together = ('library', 'game')
