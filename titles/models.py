from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=500)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="titles")
    genre = models.ManyToManyField(Genre, related_name="titles")
