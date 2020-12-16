# Generated by Django 3.1.3 on 2020-12-15 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('device_name', models.CharField(max_length=64)),
                ('model', models.CharField(default='Null', max_length=64)),
                ('theNum', models.CharField(max_length=64)),
                ('plateform', models.CharField(default='Null', max_length=64)),
                ('brand', models.CharField(max_length=64, null=True)),
                ('owner', models.CharField(default='测试', max_length=64)),
                ('status', models.CharField(default=1, max_length=64)),
                ('borrower', models.CharField(max_length=64, null=True)),
                ('UUID', models.CharField(max_length=64, null=True)),
                ('comments', models.CharField(max_length=64, null=True)),
                ('category', models.CharField(default='Null', max_length=64)),
                ('check_dev', models.CharField(default=0, max_length=64)),
                ('version', models.CharField(default='Null', max_length=64)),
                ('old_dev', models.CharField(default=0, max_length=64)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('borrow_time', models.CharField(max_length=32, null=True)),
            ],
            options={
                'db_table': 'devices',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(default='guest', max_length=64, verbose_name='用户名')),
                ('password', models.CharField(max_length=64)),
                ('role', models.CharField(default=2, max_length=32)),
                ('registe_time', models.DateTimeField(auto_now=True)),
                ('login_time', models.CharField(default='Null', max_length=64)),
                ('icon', models.CharField(default='/icon/default.png', max_length=64)),
                ('session', models.CharField(max_length=64)),
                ('comments', models.CharField(default='游客', max_length=64)),
                ('login_name', models.CharField(default='Null', max_length=64)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Dev_imgs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.ImageField(blank=True, upload_to='', verbose_name='图片')),
                ('apply_path', models.ImageField(blank=True, upload_to='', verbose_name='申请采购图片')),
                ('device_id', models.ForeignKey(default='Null', on_delete=django.db.models.deletion.CASCADE, to='createdatabase.devices')),
            ],
            options={
                'db_table': 'dev_imgs',
            },
        ),
    ]
