from django.contrib import admin

from .models import Organization, Category,\
        OrganizationDetailImages, PhoneNumber, Review, ReviewDetailImages

from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget



class OrganizationAdminForm(forms.ModelForm):
    """Form widget ckeditor"""
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Organization
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Categories"""
    list_display = ("name", "slug")
    list_display_links = ("name",)


# class ReviewInline(admin.TabularInline):
#     """Reviews"""
#     model = Review
#     extra = 1
#     readonly_fields = ("name", "email")


class OrganizationImageInline(admin.TabularInline):
    model = OrganizationDetailImages
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = "Image"


class OrganizationPhoneInline(admin.TabularInline):
    model = PhoneNumber
    extra = 1
    # readonly_fields = ("number",)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Organization"""
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [OrganizationImageInline, OrganizationPhoneInline] #, ReviewInline
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions = ["publish", "unpublish"]
    form = OrganizationAdminForm
    readonly_fields = ("get_image",)
    fieldsets = (
        (None, {
            "fields": (("slug", "title"),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"))
        }),
        (None, {
            "fields": (("year", "address"),)
        }),
        (None, {
            "classes": ("collapse",),
            "fields": (("category",),)
        }),
        (None, {
            "fields": (("budget",),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    def unpublish(self, request, queryset):
        """Unpublish"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Publish"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Publish"
    publish.allowed_permissions = ('change', )

    unpublish.short_description = "Unpublish"
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = "Poster"


# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     """Review"""
#     list_display = ("name", "email", "parent", "movie", "id")
#     readonly_fields = ("name", "email")


# @admin.register(Rating)
# class RatingAdmin(admin.ModelAdmin):
#     """Rating"""
#     list_display = ("star", "movie", "ip")


# @admin.register(OrganizationDetailImages)
class OrganizationImageAdmin(admin.ModelAdmin):
    """MovieShots"""
    list_display = ("title", "organization", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Image"


# admin.site.register(RatingStar)


class ReviewImageInline(admin.TabularInline):
    model = ReviewDetailImages
    extra = 3
    fields = ('image', )


class ReviewAdmin(admin.ModelAdmin):
    inlines = [
        ReviewImageInline
    ]
    list_display = ('author', 'organization')
    list_display_links = ('author', 'organization')


admin.site.register(Review, ReviewAdmin)

admin.site.site_title = "Django Organization"
admin.site.site_header = "Django Organization"
