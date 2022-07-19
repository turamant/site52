from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from projects.forms import ProjectForm
from projects.models import Project, Tag
from projects.utils import searchProjects, paginateProjects


def get_projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 3)
    context = {'projects': projects,
               'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)


def get_project(request, pk):
    projectObj = get_object_or_404(Project, id=pk)
    tags = projectObj.tags.all()
    return render(request, 'projects/single-project.html', {'project': projectObj, 'tags': tags})


def create_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects:projects')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


def update_project(request, pk):
    project = get_object_or_404(Project, id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:projects')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


def delete_project(request, pk):
    project = get_object_or_404(Project, id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects:projects')
    context = {'object': project}
    return render(request, 'projects/delete.html', context)


def projects_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    projects = Project.objects.filter(tags__in=[tag])
    context = {
        "projects": projects
    }

    return render(request, "projects/projects.html", context)

