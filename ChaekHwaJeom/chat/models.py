from django.db import models
from django.utils import timezone
from books.models import Book
from django.conf import settings

class Sharing(models.Model):
    book = models.OneToOneField(Book,on_delete=models.CASCADE)
    userA = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="userA",on_delete=models.CASCADE)    #현재 유저
    userB = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="userB",on_delete=models.CASCADE)    #이웃
    isFinished = models.BooleanField(default=False)

    def __str__(self):
        return str(self.book)

class Message(models.Model):
    sharing = models.ForeignKey(Sharing,on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="sender",on_delete=models.CASCADE, null = True)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="receiver",on_delete=models.CASCADE, null=True)
    sentAt = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=100)
    
    sender_isRead = models.BooleanField(default=False)
    receiver_isRead = models.BooleanField(default=False)

    objects = models.Manager()

    def save(self,**kwargs):
        if not self.id:
            self.sendAt = timezone.now()
        super(Message, self).save(**kwargs)


    class Meta:
        ordering = ['sentAt']
    
    def __str__(self):
        return self.content[:20]

class Report(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    report1 = models.BooleanField('책을 훼손해서 반납했어요',default=False)
    report2 = models.BooleanField('책을 반납하지 않아요(잠수, 연락 안받기 etc)',default=False)
    report3 = models.BooleanField('불량채팅을 했어요(나쁜 말, 못된 말 etc)',default=False)

    content = models.TextField(max_length=200,blank=True)

    def summary(self):
        return self.content[:20]