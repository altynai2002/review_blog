from time import time

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg
from django.urls import reverse

from pytils.translit import slugify


def gen_slug(s):
    """generate slug"""
    slug = slugify(s)
    return slug + '-' + str(int(time()))


class Category(models.Model):
    """Organization Category"""
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, primary_key=True, blank=True)

    def __str__(self):
        return self.name

    def save(self):
        if not self.slug:
            self.slug = gen_slug(self.name)
        super().save()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Organization(models.Model):
    """Organization characteristics"""
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=130, unique=True, blank=True)
    description = models.TextField()
    url = models.CharField(max_length=255, blank=True, null=True)
    poster = models.ImageField(upload_to='organization/')
    year = models.PositiveSmallIntegerField(default=2021, blank=True)
    address = models.CharField(max_length=255)
    budget = models.PositiveIntegerField(help_text="на одного человека в сомах")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    draft = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("org_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    def get_avg_rating(self):
        rating_items = self.reviews.all()
        values = rating_items.aggregate(avg=Avg('rating'))
        return values['avg']


class PhoneNumber(models.Model):
    """If organization has more than 1 number"""
    number = models.CharField(max_length=30, blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="phone")


class OrganizationDetailImages(models.Model):
    """Organization detail images"""
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="org_detail_img/", blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.title


class Review(models.Model):
    """Reviews or comments"""
    email = models.EmailField()
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    RATING_CHOICES = (
                (1, 1),
                (2, 2),
                (3, 3),
                (4, 4),
                (5, 5),
            )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=5000)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name="children")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"{self.author} - {self.organization}"


class ReviewDetailImages(models.Model):
    """Review detail images"""
    image = models.ImageField(upload_to="review_detail_img/", blank=True, null=True)
    organization = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')

