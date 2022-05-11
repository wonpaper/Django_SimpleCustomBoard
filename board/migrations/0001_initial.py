# Generated by Django 4.0.4 on 2022-04-29 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('member', '0002_member_update_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('no', models.AutoField(db_column='no', primary_key=True, serialize=False)),
                ('subject', models.CharField(db_column='subject', max_length=255)),
                ('content', models.TextField(blank=True, db_column='content')),
                ('read_num', models.IntegerField(db_column='read_num', default=0)),
                ('reg_date', models.DateTimeField(auto_now_add=True, db_column='reg_date')),
                ('update_date', models.DateTimeField(auto_now_add=True, db_column='update_date')),
                ('image1', models.ImageField(blank=True, db_column='image1', max_length=255, upload_to='board/image1/%Y/%m/%d/')),
                ('upfile1', models.FileField(blank=True, db_column='upfile1', max_length=255, upload_to='board/image1/%Y/%m/%d/')),
                ('member_no', models.ForeignKey(db_column='member_no', null=True, on_delete=django.db.models.deletion.SET_NULL, to='member.member')),
            ],
            options={
                'db_table': 'board',
            },
        ),
    ]