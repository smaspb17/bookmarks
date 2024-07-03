from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Action(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actions',
        verbose_name='Пользователь',
    )
    verb = models.CharField(
        max_length=255,
        verbose_name='Действие'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано'
    )
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name='target_obj',
        on_delete=models.CASCADE,
    )
    target_id = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['target_ct', 'target_id'])
        ]
        ordering = ['-created']



