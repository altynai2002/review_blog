from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, permissions as p, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .filters import OrganizationFilter
from .models import Organization, Review, Category
from .permissions import IsAuthor
from .serializers import OrganizationDetailSerializer, OrganizationListSerializer, \
    CreateUpdateOrganizationSerializer, OrganizationSerializer, ReviewSerializer, \
    CreateUpdateReviewSerializer, CategorySerializer


class MyPagination(PageNumberPagination):
    page_size = 2


class CategoriesList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

### Organization Views ###


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    pagination_class = MyPagination
    filter_backends = [DjangoFilterBackend]
    filter_class = OrganizationFilter
    filter_fields = ('category', )

    def get_serializer_class(self):
        if self.action == 'list':
            return OrganizationListSerializer
        elif self.action == 'retrieve':
            return OrganizationSerializer
        return CreateUpdateOrganizationSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'search']:
            permissions = []
        else:
            permissions = [p.IsAdminUser]
        return [permission() for permission in permissions]

    @action(methods=['get'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        if q is not None:
            queryset = queryset.filter(Q(title__icontains=q) |
                            Q(description__icontains=q))
        serializer = OrganizationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrganizationDetailView(RetrieveAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationDetailSerializer
    lookup_field = 'slug'

### Review Views ###


class ReviewList(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewCreateView(generics.CreateAPIView):
    """Create Review"""
    queryset = Review.objects.all()
    permission_classes = [p.IsAuthenticated, IsAuthor]
    serializer_class = CreateUpdateReviewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewUpdateView(UpdateAPIView):
    """Update Review"""
    queryset = Review.objects.all()
    permission_classes = [p.IsAuthenticated, IsAuthor]
    serializer_class = CreateUpdateReviewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewDeleteView(DestroyAPIView):
    """Delete Review"""
    queryset = Review.objects.all()
    permission_classes = [p.IsAuthenticated, IsAuthor]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


