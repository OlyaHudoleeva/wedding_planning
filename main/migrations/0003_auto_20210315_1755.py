# Generated by Django 3.1.4 on 2021-03-15 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210305_1853'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('sex', models.CharField(choices=[('M', 'Мужчина'), ('F', 'Женщина'), ('C', 'Ребёнок')], default='M', max_length=1)),
                ('rsvp', models.CharField(choices=[('IN', 'Приглашение не отправлено'), ('IS', 'Приглашение отправлено'), ('IA', 'Приглашение принято'), ('ID', 'Приглашение отклонено')], default='IN', max_length=2)),
                ('side', models.CharField(choices=[('G', 'Сторона жениха'), ('B', 'Сторона невесты')], default='B', max_length=1)),
            ],
        ),
        migrations.RenameField(
            model_name='task',
            old_name='task_group_id',
            new_name='task_group',
        ),
        migrations.RenameField(
            model_name='taskgroup',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('P', 'В процессе'), ('C', 'Выполнена')], default='P', max_length=1),
        ),
        migrations.AlterField(
            model_name='taskgroup',
            name='status',
            field=models.CharField(choices=[('P', 'В процессе'), ('C', 'Выполнена')], default='P', max_length=1),
        ),
    ]
