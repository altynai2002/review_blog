from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register('', OrganizationViewSet)
urlpatterns = [
    path('categories/', CategoriesList.as_view()),
    path("organization/<str:slug>/", OrganizationDetailView.as_view()),
    path('review/', ReviewList.as_view()),
    path("review/create/", ReviewCreateView.as_view()),
    path("review/update/<str:pk>/", ReviewUpdateView.as_view()),
    path("review/delete/<str:pk>/", ReviewDeleteView.as_view()),
    path('', include(router.urls)),
]
