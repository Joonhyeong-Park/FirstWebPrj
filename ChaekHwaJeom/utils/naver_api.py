import urllib.request
import urllib.parse
import json
import re

from django.conf import settings
from books.models import Book
from books.forms import BookForm, ReviewForm
from django.db.models import Q

def search_book_info(isbn):

    # client_id, client_secret KEY 가져오기
    config_secret = json.loads(open(settings.CONFIG_SECRET_FILE).read())
    client_id = config_secret['NAVER_SEARCH']['CLIENT_ID']
    client_secret = config_secret['NAVER_SEARCH']['CLIENT_SECRET']

    encText = urllib.parse.quote("{}".format(isbn))

    url = "https://openapi.naver.com/v1/search/book.json?query=" + encText 

    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id",client_id)
    req.add_header("X-Naver-Client-Secret",client_secret)
    
    response = urllib.request.urlopen(req)
    res_code = response.getcode()

    if res_code==200:
        response_body = response.read()
        response_json = response_body.decode('utf-8')
        result = json.loads(response_json)
        items = result["items"]

        for item in items:
            item['title'] = re.sub('<.+?>', '', item['title'])
            item['author'] = re.sub('<.+?>', '', item['author'])
            item['publisher'] = re.sub('<.+?>', '', item['publisher'])
            item['isbn'] = re.sub('<.+?>', '', item['isbn'])
            # item['isbn'] = item['isbn'].split(' ')[1]
            item['image'] = item['image'].split('?')[0] 
            
        return items
    else:
        print("잘못된 응답을 반환하고 있습니다")


def register_new_book(isbn,user):

    isbn = isbn.split(' ')[1]

    # 사용자가 이전에 등록한 도서인 경우, 도서 등록을 수행하지 않고 return
    if Book.objects.filter(Q(ISBN=isbn) & Q(user=user)).exists():
        state = '이미 등록하신 도서입니다'
        return state, None

    # isbn으로 해당 도서 검색
    result = search_book_info(isbn)
    item = result[0]

    # 정규표현식으로 문자열 매칭시키기
    TAG_RE = re.compile(r'<[^>]+>')

    # print(user.username)
    # print(isbn)
    # print(item['title'])
    
    book = Book.objects.create(
        user = user,
        ISBN = isbn,
        title = TAG_RE.sub('',item['title']),
        author = TAG_RE.sub('',item['author']),
        publisher = TAG_RE.sub('',item['publisher']),
        bookcover = item['image'].split('?')[0]         
    )

    state , book = '도서가 등록되었습니다', book
            
    return state, book
