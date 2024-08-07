from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4

from django.urls import reverse

User = get_user_model()


class Group(models.Model):
    """Модель хранит информацию о групповом чате"""
    uuid = models.UUIDField(default=uuid4, editable=False)
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(User)

    def __str__(self) -> str:
        return f'Group {self.name}-{self.uuid}'
    
    def get_absolute_url(self):
        return reverse('group', args=[str(self.uuid)])
    
    def add_user_to_group(self, user: User):
        "Вспомогательная функция для добавления юзера в группу и создания объекта"
        self.members.add(user)
        self.event_set.create(type='Join', user=user)
        self.save()

    def remove_user_from_group(self, user:User):
        """Функция для удаления участников группы, когда они выходят из чата"""
        self.members.remove(user)
        self.event_set.create(type='Left', user=user)
        self.save()


class Message(models.Model):
    """Модель сообщения в чате"""
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self) -> str:
        date = self.timestamp.date()
        time = self.timestamp.time()
        return f'{self.author}:-{self.content} @{date} {time.hour}: {time.minute}'
    

class Event(models.Model):
    CHOICES = [
        ('Join', 'join'),
        ('Left', 'left')
    ]
    type = models.CharField(choices=CHOICES, max_length=18)
    description = models.CharField(help_text="A description of the event that occurred",\
    max_length=50, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.description = f'{self.user} {self.type} the {self.group.name} group'
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.description}"