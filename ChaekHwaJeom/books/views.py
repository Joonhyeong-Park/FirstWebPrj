from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Book, Review, Tag
from .forms import BookForm, ReviewForm, TagForm, CommentForm
import json
import re
from accounts.models import MyUser
from utils.naver_api import search_book_info, register_new_book
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from itertools import chain
from chat.models import Message
# Create your views here.
def home(request):
    cur_user = request.user
    if request.method == "GET":
        q = request.GET.get('main')
        if q:
            books = Book.objects.filter(Q(title__icontains=q) | Q(author__icontains=q) | Q(publisher__icontains=q))
            for book in books:
                title=book.title.split('(')
                book.title = title[0]
            return render(request,'books/main_search.html',{'books':books})

    if cur_user.is_authenticated:
        return render(request,'books/base.html',{'user':cur_user}) 
    else:
        return render(request,'books/base.html') 

def query_book(request):
    if request.method == "GET":
        q = request.GET.get('main')
        if q:
            books = Book.objects.filter(Q(title__icontains=q) | Q(author__icontains=q) | Q(publisher__icontains=q))
            # print(books)
            return render(request,'books/main_search.html',{'books':books})

def edit(request, pk):
    post = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now
            post.save()
            return redirect('detail', pk=post.pk)
    else:
        form = BookForm(instance=post)
    return render(request, 'books/edit.html', {'form': form})

def delete(request, pk):
    post = get_object_or_404(Content, pk=pk)
    post.delete()
    return redirect('home')

def user_library(request):
    user = request.user

    if user.is_authenticated:
        books = Book.objects.filter(user=user)
        for book in books:
            review = get_object_or_404(Review,pk=book)

            title=book.title.split('(')
            book.title = title[0]
            book.review = review
            book.review_rate = range(review.rate)

        return render(request,'books/user_library.html',{'user':user,'books':books})
    else:
        return redirect('login')

def book_search(request):
    if request.method == "GET":
        # option = request.GET.get('option')
        q = request.GET.get('query')
        
        if q is None or q == '':
            return render(request,'books/book_search.html')

        # ?????? ?????? ??????
        search_result = search_book_info(q)
        index = 0
        
        for book in search_result:
            book['title'] = book['title'].split('(')[0]
            # book['option'] = option
            book['index'] = index
            index += 1

        paginator = Paginator(search_result,5)
        page = request.GET.get('page')
        books = paginator.get_page(page)

        book_form = BookForm()
        review_form = ReviewForm()

        return render(request,'books/book_search.html',{'books':books,'book_form':book_form, 'review_form': review_form})

    return redirect('book_search')

def book_register(request):
    user = request.user

    if request.method == "POST":
        isbn = request.POST.get('isbnvalue')        # ?????? ISBN value
        status = request.POST.get('status')         # ?????? ?????? ??????
        review = request.POST.get('book_review')    # ?????? ??????
        star_rate = request.POST.get('review-star') # ?????? ??????

        state, book = register_new_book(isbn,user)
        print(state)

        if book:
            # ???????????? ????????? ?????? ?????? ?????? ????????? ??????
            book.status = status                        
            book.save()

            new_review = Review.objects.create(
                book = book,
                book_review = review,
                rate = star_rate,
            )
            new_review.save()

            return redirect('book_search')

    return redirect('book_search')


def like(request):
    pk = request.POST.get('pk', None)
    # book = get_object_or_404(Book, pk=pk) 
    # book.title = book.title.split('(')[0]   
    # neighbor = book.user
    # posts = Review.objects.get(book=book)
    posts = get_object_or_404(Review, pk=pk)
    user = request.user
    if posts.likes_user.filter(email=user.email).exists():
        posts.likes_user.remove(user)
        message = '????????? ??????'
    else:
        posts.likes_user.add(user)
        message = '?????????'
    context = {'likes_count':posts.count_likes_user(), 'message': message}
    return HttpResponse(json.dumps(context), content_type="application/json")

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)       # ????????? ?????? ??????
    
    # ?????? split ?????? ????????????????????? '()' ?????? ?????? ??????, book.subtitle ????????? html??? ?????? ???
    book.title = book.title.split('(')[0]   
    # print(book.get_status_display())
    print(book.status) 
    neighbor = book.user

    review = Review.objects.get(book=book)      # ????????? ?????? review ??????
    
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = review
            comment.text = comment_form.cleaned_data.get("text")
            comment.save()

            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    
    return render(request,'books/book_detail.html',{
                    'neighbor' : neighbor, 
                    'book': book, 
                    'review':review,
                    'rate':range(review.rate),
                    'rate_blank': range(5-review.rate),
                    'comment_form': comment_form
                    })

def tag_add(request,pk):
    book = get_object_or_404(Book,pk=pk)
    tag_form = TagForm(request.POST)

    if tag_form.is_valid():
        tag = tag_form.save(commit=False)
        # ??????????????? ?????? ????????? ?????? ???????????? ?????? ??? ????????? ????????????, ?????? ?????? ?????? ??????
        tag, created = Tag.objects.get_or_create(name=tag.name)
        # book????????? tag ??????
        book.tags.add(tag)     

        return redirect('book_detail',pk=pk)

def tag_detail(request,pk):
    tag = get_object_or_404(Tag,pk=pk)
    tag_posts = tag.book_set.all()

    return render(request, 'books/tag_detail.html',{'tag':tag, 'tag_posts':tag_posts})

    
def tag_delete(request,pk,tag_pk):
    book = get_object_or_404(Book,pk=pk)
    tag = get_object_or_404(Tag,pk=tag_pk)

    # book ???????????? tag ??????
    book.tags.remove()

    return redirect('book_detail',pk=pk)
  
def service_manual(request):
    return render(request, 'books/service_manual.html')

def neighbor_library(request):
    cur_user = request.user
    if cur_user.is_authenticated:
        result = []
        dong = MyUser.objects.filter(dong__icontains=cur_user.dong).exclude(email=cur_user.email)
        for d in dong:                              # ???????????? ???????????? ?????? ?????? ???????????? user
            # print(d.username)
            # print(Book.objects.filter(user=d).count())
            books = d.bookuser.all()
            books_cnt = books.count()
            if books_cnt > 0 :
                info = {}
                info['user'] = d
                info['books'] = d.bookuser.all()
                info['books_cnt'] = books_cnt
                result.append(info)

        result.sort(key=lambda x:x['books_cnt'],reverse=True)
        print(result)
        if not result:
            print('noneeeee')
        return render(request,'books/neighbor_library.html',{'neighbor':result})
    else:
        return redirect('login')

    return render(request, 'books/neighbor_library.html')
