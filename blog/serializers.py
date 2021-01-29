from rest_framework import serializers, permissions as p

from .models import Organization, PhoneNumber, Review, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhoneNumber
        fields = ('number',)


### Review  Serializers ###


class CreateUpdateReviewSerializer(serializers.ModelSerializer):
    """CRU of Review"""
    author = serializers.CharField(read_only=True)
    permission_classes = [p.IsAuthenticated]

    class Meta:
        model = Review
        fields = "__all__"

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзывов"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("id", "author", "text", "children", "rating")

    def _get_image_url(self, obj):
        request = self.context.get('request')
        image_obj = obj.images.first()
        if image_obj is not None and image_obj.image:
            url = image_obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation



### Organization serializers ###


class OrganizationSerializer(serializers.ModelSerializer):
    """List of organizations"""

    class Meta:
        model = Organization
        fields = ("title", "category", "poster", "budget")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = instance.get_avg_rating()
        return representation


class OrganizationListSerializer(serializers.ModelSerializer):
    """List of organizations"""

    class Meta:
        model = Organization
        fields = ("title", "category", "poster", "budget")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = instance.get_avg_rating()
        return representation


class OrganizationDetailSerializer(serializers.ModelSerializer):
    """Organization's details"""
    title = serializers.CharField(read_only=True)
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    reviews = ReviewSerializer(many=True)
    lookup_field = 'slug'

    class Meta:
        model = Organization
        exclude = ("draft", "id", 'slug')

    def _get_image_url(self, obj):
        request = self.context.get('request')
        image_obj = obj.images.first()
        if image_obj is not None and image_obj.image:
            url = image_obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        representation['phone'] = PhoneSerializer(instance.phone.all(), many=True).data
        representation['rating'] = instance.get_avg_rating()
        return representation


class CreateUpdateOrganizationSerializer(serializers.ModelSerializer):
    """CRU of Organization"""
    class Meta:
        model = Organization
        fields = ['title', 'poster', 'address', 'description', 'budget', 'category']


