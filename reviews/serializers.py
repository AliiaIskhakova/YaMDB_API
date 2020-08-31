from rest_framework import serializers
from django.shortcuts import get_object_or_404

from reviews.models import Comment, Review
from titles.models import Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review

    def validate(self, data):
        title = get_object_or_404(
            Title, id=self.context['view'].kwargs['title_id'])
        review = Review.objects.filter(
            title=title, author=self.context['request'].user)
        if self.context['request'].method == 'PATCH':
            return data
        if review.exists():
            raise serializers.ValidationError(
                "Вы уже оставляли отзыв на это произведение.")
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment
