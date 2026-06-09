from django.conf import settings
from django.db import models


class Project(models.Model):
    STATUS_OPEN = 'open'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Открыт'),
        (STATUS_CLOSED, 'Завершён'),
    ]

    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    status = models.CharField(
        'Статус', max_length=10, choices=STATUS_CHOICES, default=STATUS_OPEN,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_projects',
        verbose_name='Автор',
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='joined_projects',
        blank=True,
        verbose_name='Участники',
    )
    favorited_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='favorite_projects',
        blank=True,
        verbose_name='В избранном у',
    )
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_open(self):
        return self.status == self.STATUS_OPEN

    def short_description(self, length=120):
        if len(self.description) <= length:
            return self.description
        return self.description[:length] + '…'
