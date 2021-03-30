from django.contrib import admin
from .models import Book, Review, Tag, Comment
from .forms import ReviewForm, ReviewAdminForm

# Register your models here.
admin.site.register(Book)
admin.site.register(Comment)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm 

admin.site.register(Tag)