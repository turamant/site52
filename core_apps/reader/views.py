import os
from wsgiref.util import FileWrapper

from django.conf import settings
from django.core import serializers
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import BookForm
from .models import Book


def download_file(request, file_name):
    file_path = os.path.join(settings.PRIVATE_STORAGE_ROOT, file_name)
    filename = os.path.basename(file_path)
    chunk_size = 8192
    response = StreamingHttpResponse(
        FileWrapper(open(file_path, 'rb'), chunk_size),
        content_type="application/octet-stream"
    )
    response['Content-Length'] = os.path.getsize(file_path)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def json_data(request):
    data_book = Book.objects.all()
    data = serializers.serialize('json', data_book)
    return JsonResponse(data, safe=False)


class BookListView(ListView):
    model = Book
    template_name = 'reader/index.html'
    paginate_by = 3


class BookDetailView(DetailView):
    model = Book
    template_name = 'reader/book_detail.html'


class BookPython(ListView):
    model = Book
    template_name = 'reader/pythons.html'
    queryset = Book.objects.filter(genre='Python language').all()
    context_object_name = 'books'
    paginate_by = 4


class BookBest(ListView):
    model = Book
    template_name = 'reader/the_best.html'
    queryset = Book.objects.filter(rating__gt=3).all()
    context_object_name = 'books'
    paginate_by = 4


class BookCreateView(CreateView):
    model = Book
    template_name = 'reader/create.html'
    fields = '__all__'


class BookEditView(UpdateView):
    model = Book
    template_name = 'reader/edit.html'
    fields = '__all__'


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'reader/delete.html'
    success_url = reverse_lazy('reader:index')
