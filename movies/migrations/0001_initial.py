# Generated by Django 5.0.7 on 2024-12-29 12:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Genres",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Movies",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(db_index=True, max_length=100, unique=True)),
                ("overview", models.TextField(blank=True, max_length=500)),
                ("release_date", models.DateField(blank=True, null=True)),
                ("country", models.CharField(max_length=100)),
                (
                    "poster",
                    models.ImageField(
                        blank=True,
                        default="movie_posters/default-poster.jpg",
                        null=True,
                        upload_to="movie_posters/",
                    ),
                ),
                ("adult", models.BooleanField(default=False)),
                ("average_rating", models.FloatField(default=0.0)),
                (
                    "genres",
                    models.ManyToManyField(related_name="movies", to="movies.genres"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WatchLater",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("added_at", models.DateTimeField(auto_now_add=True)),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="watchlater",
                        to="movies.movies",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="watchlater",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="movies",
            index=models.Index(
                fields=["title", "release_date", "country", "poster", "average_rating"],
                name="movies_movi_title_b17055_idx",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="watchlater",
            unique_together={("user", "movie")},
        ),
    ]
