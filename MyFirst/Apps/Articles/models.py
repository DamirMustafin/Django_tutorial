from django.db import models

import datetime
from django.utils import timezone

class Article(models.Model):
    article_title = models.CharField('название статьи', max_length=200, help_text="Название статьи")
    article_text = models.TextField('текст статьи')
    pub_date = models.DateTimeField('дата публикации')

    def __str__(self):
        return  self.article_title

    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days = 7))

    def get_absolute_url(self):
        return reversed('model-detail-view', args=[str(self.id)])

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author_name = models.CharField('имя автора', max_length=50, help_text="Имя автора комментария")
    comment_text = models.CharField('текст комментария', max_length=200)

    def __str__(self):
        return  self.author_name

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарий'