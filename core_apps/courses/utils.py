from .models import Course, Subject
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchProjects(request):

    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    subjects = Subject.objects.filter(title__icontains=search_query)

    courses = Course.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(subjects__in=subjects)
    )
    return courses, search_query