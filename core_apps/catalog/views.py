from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views import generic

from .models import Book, BookInstance, Author, Genre


@login_required
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    num_genre = Genre.objects.all().count
    books_word = Book.objects.filter(title__contains='Онегин').count()
    context = {'num_books': num_books, 'num_instances': num_instances, 'num_genre': num_genre,
               'num_instances_available': num_instances_available, 'num_authors': num_authors,
               'books_word': books_word, 'num_visits': num_visits}

    return render(request, 'catalog/index.html', context=context)


class MyBookListView(LoginRequiredMixin, generic.ListView):
    """файл долджен называться - book_list.html, иначе нужено бдет указывать путь к шаблону"""
    model = Book


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 3


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some'] = "This is cool!"
        return context


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksAll(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
