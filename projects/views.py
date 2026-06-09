from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProjectForm
from .models import Project


def project_list(request):
    projects = Project.objects.select_related('author').all()
    paginator = Paginator(projects, 12)
    page = paginator.get_page(request.GET.get('page'))
    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(
            request.user.favorite_projects.values_list('pk', flat=True)
        )
    return render(request, 'projects/project_list.html', {
        'page_obj': page,
        'favorite_ids': favorite_ids,
    })


def project_detail(request, pk):
    project = get_object_or_404(
        Project.objects.select_related('author').prefetch_related('participants'),
        pk=pk,
    )
    is_owner = request.user.is_authenticated and request.user == project.author
    is_participant = (
        request.user.is_authenticated
        and project.participants.filter(pk=request.user.pk).exists()
    )
    is_favorite = (
        request.user.is_authenticated
        and project.favorited_by.filter(pk=request.user.pk).exists()
    )
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'is_owner': is_owner,
        'is_participant': is_participant,
        'is_favorite': is_favorite,
    })


@login_required
def project_create(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.author = request.user
        project.save()
        messages.success(request, 'Проект опубликован.')
        return redirect('projects:detail', pk=project.pk)
    return render(request, 'projects/project_form.html', {
        'form': form,
        'title': 'Создать проект',
        'submit_label': 'Опубликовать',
    })


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, author=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        messages.success(request, 'Изменения сохранены.')
        return redirect('projects:detail', pk=project.pk)
    return render(request, 'projects/project_form.html', {
        'form': form,
        'project': project,
        'title': 'Редактировать проект',
        'submit_label': 'Сохранить изменения',
    })


@login_required
@require_POST
def project_join(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.author == request.user:
        messages.info(request, 'Вы автор этого проекта.')
    elif project.status != Project.STATUS_OPEN:
        messages.error(request, 'Проект уже завершён.')
    elif project.participants.filter(pk=request.user.pk).exists():
        messages.info(request, 'Вы уже в команде.')
    else:
        project.participants.add(request.user)
        messages.success(request, 'Вы присоединились к проекту.')
    return redirect('projects:detail', pk=pk)


@login_required
@require_POST
def project_complete(request, pk):
    project = get_object_or_404(Project, pk=pk, author=request.user)
    project.status = Project.STATUS_CLOSED
    project.save()
    messages.success(request, 'Проект завершён.')
    return redirect('projects:detail', pk=pk)


@login_required
@require_POST
def toggle_favorite(request, pk):
    from django.urls import reverse

    project = get_object_or_404(Project, pk=pk)
    if project.favorited_by.filter(pk=request.user.pk).exists():
        project.favorited_by.remove(request.user)
        messages.info(request, 'Проект убран из избранного.')
    else:
        project.favorited_by.add(request.user)
        messages.success(request, 'Проект добавлен в избранное.')
    next_url = request.POST.get('next') or reverse('projects:list')
    return redirect(next_url)


@login_required
def favorites_list(request):
    projects = request.user.favorite_projects.select_related('author').all()
    paginator = Paginator(projects, 12)
    page = paginator.get_page(request.GET.get('page'))
    favorite_ids = set(projects.values_list('pk', flat=True))
    return render(request, 'projects/favorites.html', {
        'page_obj': page,
        'favorite_ids': favorite_ids,
    })
