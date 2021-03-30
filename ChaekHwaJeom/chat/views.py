from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.db.models import Q
from utils.slack import slack_notify

from .models import Message, Report, Sharing
from .forms import MessageForm, ReportForm
from accounts.models import MyUser
from books.models import Book


def chat(request):
    user = request.user

    # 현 사용자와 거래 내역이 있는 user로만!
    # all_user = MyUser.objects.all().exclude(pk=user.pk)
    # nested list (list > dict > list)
    # ongoing = [
    #     { 
    #         'username': ,
    #         'sharing_info': list( dict {pk, book_title}),
    #     },
    #         ...
    # ]
    sharing = Sharing.objects.filter(Q(userA=user)|Q(userB=user))
    if sharing == None:
        return render(request,'chat/chat.html',{'user':user})

    ongoing = list()
    finished = list()

    all_user = dict()

    for s in sharing:
        if s.userA == user:
            username = s.userB.nickname
            all_user[s.userB.pk] = username
        else:
            username = s.userA.nickname
            all_user[s.userA.pk] = username

        s.book.title = s.book.title.split('(')[0]

        new_neighbor = True
        # 거래 중인 도서 (ongoing)
        if s.isFinished == False:
            for item in ongoing:
                if item['username'] == username:
                    # list에 존재하는 요소인 경우, book list를 append
                    new_neighbor = False
                    item['sharing_info'].append(
                        {s.pk : s.book}
                    )

        # 거래 완료된 도서 (finished)
        else:
            for item in finished:
                if item['username'] == username:
                    new_neighbor = False
                    item['sharing_info'].append(
                        {s.pk : s.book}
                    )

        # list에 존재하지 않던 요소인 경우, 새로운 항목을 append
        if new_neighbor == True:
            sharing_info = list()
            sharing_info.append(
                {s.pk : s.book}
            )

            chat = dict()
            chat['username'] = username
            chat['sharing_info'] = sharing_info
            
            if s.isFinished == False:
                ongoing.append(chat)
            else:
                finished.append(chat)
               
    # print(ongoing)
    # print(finished)
    # for item in finished:
    #     for i in item['sharing_info']:
    #         for key,value in i.items():
    #             print(type(key))
    #             print(value)
    #             print(type(value))

    report_form = ReportForm()

    print(all_user)
    return render(request,'chat/chat.html',{'sharing':'True','ongoing':ongoing, 'finished':finished,'all_user':all_user,'report_form':report_form})

def sharing(request,book_pk,neighbor_pk):
    
    user = request.user
    neighbor = get_object_or_404(MyUser,pk=neighbor_pk)
    book = get_object_or_404(Book,pk=book_pk)

    try:
        q1 = Sharing.objects.get(Q(userA=user)&Q(userB=neighbor)&Q(book=book))
    except Sharing.DoesNotExist:
        q1 = None
        
    try:
        q2 = Sharing.objects.get(Q(userB=user)&Q(userA=neighbor)&Q(book=book))
    except Sharing.DoesNotExist:
        q2 = None

    if q1:
        if q1.isFinished == False:
                print('거래 중인 도서입니다')
        else:
            q1.isFinished = False
            print('거래가 완료된 도서입니다')
        return redirect('chat')

    elif q2:
        if q2.isFinished == False:
                print('거래 중인 도서입니다')
        else:
            q2.isFinished = False
            print('거래가 완료된 도서입니다')
        return redirect('chat')
        
    else:
        sharing = Sharing.objects.create(
            userA = user,
            userB = neighbor,
            book = book,
            isFinished = False
        )
        return redirect('listMessage',sharing.pk)

def set_sharing_state(request,sharing_pk):
    sharing = get_object_or_404(Sharing,pk=sharing_pk)

    if sharing.isFinished == False:
        sharing.isFinished = True
        sharing.save()
        return redirect('chat')

    return redirect('chat')

def chatroom(request,sharing_pk):
    # 채팅 메인페이지에서 채팅 페이지로 이동
    print(sharing_pk)
    
    sharing = get_object_or_404(Sharing,pk=sharing_pk)
    message_list = Message.objects.filter(sharing=sharing)
    received = message_list.filter(receiver=request.user)
    for r in received:
        r.receiver_isRead = True
        r.save()

    return redirect('listMessage',sharing_pk)

def message(request,pk):
    # 채팅방에 접속하면, 
    # 내가 마지막으로 전송한 메세지 이전의 메세지들을 모두 읽음 처리
    
    cur_user = request.user
    sharing = Sharing.objects.get(pk=pk)
    if sharing.userA == cur_user:
        receiver = sharing.userB.nickname
    else:
        receiver = sharing.userA.nickname

    message_list = Message.objects.filter(sharing=sharing)          # 메세지 log

    received = message_list.filter(receiver=request.user)   # 받은 메세지
    sent = message_list.filter(sender=request.user)         # 보낸 메세지

    form = MessageForm()
    if request.method == 'POST':
        content = request.POST.get('content')

        message = Message.objects.create(
            sharing = sharing,
            sender = cur_user,
            content = content,
            receiver_isRead = False,
            sender_isRead = True
        )
        if sharing.userA == cur_user:
            message.receiver = sharing.userB
        else:
            message.receiver = sharing.userA
        message.save()

    return render(request,'chat/message.html',{'messages':message_list,'receiver': receiver, 'form':form})


def chat_guide(request):
    return render(request,'report/chat_guideline.html')

def service_guide(request):
    return render(request,'report/service_guideline.html') 


def report(request):
    if request.method == 'POST':
        report_user_pk = request.POST.get('user')
        report1 = request.POST.get('report1')
        report2 = request.POST.get('report2')
        report3 = request.POST.get('report3')
        content = request.POST.get('content')

        report_user = get_object_or_404(MyUser,pk=report_user_pk)
        print(report_user.nickname)
        if report1 == None:
            report1 = False
        if report2 == None:
            report2 = False
        if report3 == None:
            report3 = False

        report = Report.objects.create(
            user = report_user,
            report1 = report1,
            report2 = report2,
            report3 = report3,
            content = content
        )
        # slack에 신고 접수 알림 보내기
        attachments = [{
            "color": "#FF0000",
            "title": "신고접수 알림",
            "text": "{}".format(report.content)
            }]
        slack_message = "[신고접수] {}에 대한 신고가 접수되었습니다.".format(report_user.nickname)
        slack_notify(slack_message,"#random",username='신고 접수봇',attachments=attachments)

        return redirect('chat')