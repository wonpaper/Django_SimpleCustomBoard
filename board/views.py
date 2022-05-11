from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse
from .models import Board
from member.models import Member
import datetime, os, random


def index(request):
    #return render(request, 'board/board_list.html')
    return redirect('board|board_list')


def board_list(request):
    context = {}
    boards = Board.objects.all().order_by('-no')
    context['boards'] = boards
    #print(boards)
    return render(request, 'board/board_list.html', context)


def board_detail(request, no):
    context = {}
    board = Board.objects.get(pk=no)
    if board is not None:
        read_num = board.read_num
        board.read_num = read_num + 1
        board.save()

        context['board'] = board
        return render(request, 'board/board_detail.html', context)
    else:
        return redirect('board/index.html')


def board_write(request):
    context = {}
    members = Member.objects.all()
    context['members'] = members

    if request.method=='GET':
        return render(request, 'board/board_write.html', context)
    elif request.method=='POST':

        member_no = request.POST['member_no']
        subject = request.POST['subject']
        content = request.POST['content']

        image1 = ''
        upfile1 = ''

        this_date = str(datetime.datetime.today().year) + "_" + str(datetime.datetime.today().month) + "_" + str(datetime.datetime.today().day)

        if 'image1' in request.FILES:
            uploaded_file = request.FILES['image1']
            name_old = uploaded_file.name
            name_ext = os.path.splitext(name_old)[1]
            name_new = 'A' + this_date + '_' + str(random.randint(100000000,999999999))

            fs = FileSystemStorage(location='media/board/images')
            new_file = fs.save(name_new + name_ext, uploaded_file)
            image1 = name_new + name_ext

        if 'upfile1' in request.FILES:
            uploaded_file = request.FILES['upfile1']
            name_old = uploaded_file.name
            name_ext = os.path.splitext(name_old)[1]
            name_new = 'A' + this_date + '_' + str(random.randint(100000000,999999999))

            fs = FileSystemStorage(location='media/board/files')
            new_file = fs.save(name_new + name_ext, uploaded_file)
            upfile1 = name_new + name_ext

        board = Board(member_no=Member.objects.get(pk=member_no), subject=subject, content=content, read_num=0, image1=image1, upfile1=upfile1)
        board.save()

#        context['message'] = "글을 등록하였습니다."
#        context['boards']  = Board.objects.all().order_by('-no')
#        return render(request, 'board/board_list.html', context)
        return redirect('/board/list/')


def file_download(request):
    path = request.GET['path']
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    if os.path.exists(file_path):
        binary_file = open(file_path, 'rb')
        response = HttpResponse(binary_file.read(), content_type="application/octet-stream; charset=utf-8")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    else:
        message = '알 수 없는 오류가 발행하였습니다.'
        return HttpResponse("<script>alert('"+ message +"');history.back()'</script>")


def board_update(request, no):
    if request.method=='GET':
        context = {}
        board = Board.objects.get(no=no)
        members = Member.objects.all()
        context['board'] = board
        context['members'] = members
        return render(request, 'board/board_update.html', context)
    elif request.method=='POST':

        subject = request.POST['subject']
        content = request.POST['content']
        member_no = request.POST['member_no']

        board = Board.objects.get(no=no)
        member = Member.objects.get(id=member_no)

        image1 = board.image1
        upfile1 = board.upfile1

        this_date = str(datetime.datetime.today().year) + "_" + str(datetime.datetime.today().month) + "_" + str(datetime.datetime.today().day)

        old_image1_del = request.POST.get('old_image1_del', '')
        if old_image1_del == 'y':
            fs = FileSystemStorage(location='media/board/images')
            furl = board.image1.url.split('/')[2]
            fs.delete(furl)
            image1 = ''

        old_upfile1_del = request.POST.get('old_upfile1_del', '')
        if old_upfile1_del == 'y':
            fs = FileSystemStorage(location='media/board/files')
            furl = board.upfile1.url.split('/')[2]
            fs.delete(furl)
            upfile1 = ''

        if 'image1' in request.FILES:

            if board.image1 != "":
                fs = FileSystemStorage(location='media/board/images')
                furl = board.image1.url.split('/')[2]
                fs.delete(furl)

            uploaded_file = request.FILES['image1']
            name_old = uploaded_file.name
            name_ext = os.path.splitext(name_old)[1]
            name_new = 'A' + this_date + '_' + str(random.randint(100000000,999999999))

            fs = FileSystemStorage(location='media/board/images')
            fs.save(name_new + name_ext, uploaded_file)
            image1 = name_new + name_ext

        if 'upfile1' in request.FILES:
            if board.upfile1 != "":
                fs = FileSystemStorage(location='media/board/files')
                furl = board.upfile1.url.split('/')[2]
                fs.delete(furl)

            uploaded_file = request.FILES['upfile1']
            name_old = uploaded_file.name
            name_ext = os.path.splitext(name_old)[1]
            name_new = 'A' + this_date + '_' + str(random.randint(100000000,999999999))

            fs = FileSystemStorage(location='media/board/files')
            fs.save(name_new + name_ext, uploaded_file)
            upfile1 = name_new + name_ext

        board.member_no = member
        board.subject = subject
        board.content = content
        board.update_date = datetime.datetime.now()
        board.image1 = image1
        board.upfile1 = upfile1
        board.save()

        return redirect('/board/update/' + str(no) + '/')


def board_delete(request, no):
    context = {}
    board = Board.objects.get(no=no)

    if board.image1 != '':
        fs = FileSystemStorage(location='media/board/images')
        furl = board.image1.url.split('/')[2]
        fs.delete(furl)
    if board.upfile1 != '':
        fs = FileSystemStorage(location='media/board/files')
        furl = board.upfile1.url.split('/')[2]
        fs.delete(furl)

    board.delete()

    boards = Board.objects.all().order_by('-no')
    context['boards'] = boards
    context['message'] = "해당 글을 정상적으로 삭제하였습니다."
    return render(request, 'board/board_list.html', context)