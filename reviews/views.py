from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Comment, Review
from reviews.permissions import IsAuthenticatedOrAdminOrModeratorOrAuthor
from reviews.serializers import CommentSerializer, ReviewSerializer
from titles.models import Title


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrAdminOrModeratorOrAuthor, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return Review.objects.filter(title=title).all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrAdminOrModeratorOrAuthor, ]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return Comment.objects.filter(review=review).all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)
