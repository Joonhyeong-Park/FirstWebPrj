from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import MyUser
from urllib.parse import urlparse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# from accounts.models import MyUser
from django.conf import settings

def file_path(instance,filename):
    extension = filename.split('.')[-1]
    isbn=instance.ISBN

    return 'covers/%s.%s' %(isbn,extension)

# Create your models here.
class Book(models.Model):

    STATUS_CHOICES = (
        ('대여 가능','대여 가능'),
        ('예약 중','예약 중'),
        ('대여 중','대여 중'),
        ('대여 불가능','대여 불가능'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="bookuser",on_delete=models.CASCADE,blank=False)

    ISBN = models.CharField(max_length=13,blank=False)
    title = models.CharField('도서명',max_length=50)
    author = models.CharField('저자',max_length=30, blank=True)
    publisher = models.CharField('출판사',max_length=30,blank=True)
    status = models.CharField('상태',choices=STATUS_CHOICES,default='대여 가능',max_length=10)
    bookcover = models.URLField(max_length=400,blank=True)
    stored_at = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField('Tag',blank=True)

    class Meta:
        ordering = ['-stored_at']

    def __str__(self):
        return self.title 


class Review(models.Model):
    book = models.OneToOneField(Book,on_delete=models.CASCADE,primary_key=True)
    book_review=models.TextField('리뷰',max_length=100,blank=True)
    rate=models.IntegerField(
        '별점',
        validators=[MinValueValidator(1),MaxValueValidator(5)],
        default=1)
    # like_count = models.PositiveIntegerField(default=0,null=True)
    likes_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL, # this is preferred than just 'User'
        blank=True, # blank is allowed
        related_name='likes_user'
    )
    def count_likes_user(self): # total likes_user
        return self.likes_user.count()



class Comment(models.Model):
    objects = models.Manager()
    post = models.ForeignKey('Review', on_delete=models.CASCADE)
    text = models.TextField(default='')
    created_date = models.DateTimeField(default=timezone.now)

    
class Tag(models.Model):
    name = models.CharField('해시태그',max_length=15)

    def __str__(self):
        return self.name


