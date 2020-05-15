from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
import uuid

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book genre")

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=200, help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    language = models.ForeignKey('language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def display_genre(self):
        return ', ' .join([ genre.name for genre in self.genre.all() [:3]])
    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # UUIDField используется для поля id, чтобы установить его как primary_key для этой модели.
    # Этот тип поля выделяет глобальное уникальное значение для каждого экземпляра
    # (по одному для каждой книги, которую вы можете найти в библиотеке).

    # DateField используется для данных due_back (при которых ожидается, что книга появится после заимствования или обслуживания).
    # Это значение может быть blank или null (необходимо, когда книга доступна).
    # Метаданные модели (Class Meta) используют это поле для упорядочивания записей, когда они возвращаются в запросе.

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reversed'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    # status - это CharField, который определяет список choice/selection.
    # Как вы можете видеть, мы определяем кортеж, содержащий кортежи пар ключ-значение и передаем его аргументу выбора.
    # Значение в key/value паре - это отображаемое значение, которое пользователь может выбрать, а ключи - это значения,
    # которые фактически сохраняются, если выбрана опция.
    # Мы также установили значение по умолчанию «m» (техническое обслуживание),
    # поскольку книги изначально будут созданы недоступными до того, как они будут храниться на полках.

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return '%s (%s)' % (self.id, self.book.title)

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        return reverse ('author-detail', args=[str(self.id)])

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)
