from django import forms
from .models import Book, Review, Comment, Tag
from .widgets import starWidget

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['status']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['book_review','rate',]

class ReviewAdminForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['book', 'rate', 'book_review']
        # widgets = {
        #     'rate': starWidget,
        # }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

