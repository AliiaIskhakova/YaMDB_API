from rest_framework import serializers

from .models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("name", "slug",)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ("name", "slug",)
        model = Genre


class TitleCreateSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(slug_field='slug', required=False, queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug', required=False, queryset=Genre.objects.all(), many=True)
    
    class Meta:
        fields = "__all__"
        model = Title

class TitleListSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)
    
    class Meta:
        fields = "__all__"
        model = Title

