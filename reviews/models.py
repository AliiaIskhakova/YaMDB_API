from django.contrib.auth import get_user_model
from django.db import models

from titles.models import Title

User = get_user_model()


class Review(models.Model):

    SCORE_CHOICES = (
        (1, '1'), (2, '2'), (3, '3'),
        (4, '4'), (5, '5'), (6, '6'),
        (7, '7'), (8, '8'), (9, '9'),
        (10, '10'))

    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True, db_index=True)
    score = models.IntegerField(choices=SCORE_CHOICES, default="0")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews")
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return "{:.50}".format(self.text)


class Comment(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True, db_index=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments")
    
    def __str__(self):
        return "{:.50}".format(self.text)
