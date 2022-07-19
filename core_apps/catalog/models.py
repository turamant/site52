from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import uuid


class Genre(models.Model):
    """Модель Жанр"""
    name = models.CharField(max_length=200, help_text="Введите жанр книги(т.к. Лирика, Поэзия и др.)")

    def __str__(self):
        return self.name


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Введите язык оргигинала книги(т.к.English, French, Russian)")

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Модель Книга (вообще , а не реальная копия книги).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Коротка аннотация содержания книги")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 символов <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Выбрать жанр книги")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)


    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog:book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """
    Модель конкретной книги(т.е. та которая может быть взята в аренду в библиотеке).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID для конкретной книги")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Обслуживание'),
        ('o', 'На руках(в аренде)'),
        ('a', 'Доступно'),
        ('r', 'Зарезервировано'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

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
    """
    Модель автора
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name']

    def get_absolute_url(self):
        return reverse('catalog:author-detail', args=[str(self.id)])

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)


