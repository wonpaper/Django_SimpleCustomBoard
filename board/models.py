from django.db import models
from member.models import Member


class Board(models.Model):
    no = models.AutoField(db_column='no', primary_key=True)
    member_no = models.ForeignKey(Member, db_column='member_no', on_delete=models.SET_NULL, null=True)
    subject = models.CharField(db_column='subject', max_length=255)
    content = models.TextField(db_column='content', blank=True)
    read_num = models.IntegerField(db_column='read_num', default=0)
    reg_date = models.DateTimeField(db_column='reg_date', auto_now_add=True)
    update_date = models.DateTimeField(db_column='update_date', auto_now_add=True)
#    image1 = models.ImageField(db_column='image1', upload_to='board/image1/%Y/%m/%d/', max_length=255, blank=True)
#    upfile1 = models.FileField(db_column='upfile1', upload_to='board/upfile1/%Y/%m/%d/', max_length=255, blank=True)

    image1 = models.ImageField(db_column='image1', max_length=255, blank=True)
    upfile1 = models.FileField(db_column='upfile1', max_length=255, blank=True)

    class Meta:
        db_table = 'board'

    def __str__(self):
        return '제목: ' + self.subject + ', 이름: ' + self.member_no.name