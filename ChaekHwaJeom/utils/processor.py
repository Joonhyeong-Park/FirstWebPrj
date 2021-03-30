from books.models import Book
from accounts.models import MyUser
from chat.models import Message

def nav_context_processor(request):
    user = request.user.is_authenticated
    context = {}
    if user:
        books_cnt = Book.objects.filter(user=request.user).count()
        message = Message.objects.filter(receiver=request.user)

        isRead = True
        for m in message:
            if m.receiver_isRead == False:
                isRead = False
                break

        context = {
            'isRead': isRead,
            'books_cnt' : books_cnt
        }

    return context