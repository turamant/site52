from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    model = Book
