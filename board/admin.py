from django.contrib import admin
from .models import Board


class BoardAdmin(admin.ModelAdmin):
    # 내가 출력하고 싶은 제목명인 필드명 subject 와 글쓴이 name 을 표시한다.
    list_display = ('subject', 'member_no')


admin.site.register(Board, BoardAdmin)

