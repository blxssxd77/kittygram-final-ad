from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from .forms import CustomPasswordChangeForm, LoginForm, ProfileEditForm, RegistrationForm
from .models import User


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('projects:list')


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.user.is_authenticated:
        return redirect('projects:list')
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Регистрация прошла успешно. Войдите в систему.')
        return redirect('users:login')
    return render(request, 'users/register.html', {'form': form})


def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    projects = user.authored_projects.all()
    is_owner = request.user.is_authenticated and request.user.pk == user.pk
    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(
            request.user.favorite_projects.values_list('pk', flat=True)
        )
    return render(request, 'users/profile.html', {
        'profile_user': user,
        'projects': projects,
        'is_owner': is_owner,
        'favorite_ids': favorite_ids,
    })


@login_required
def profile_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user != user:
        return redirect('users:profile', pk=pk)
    form = ProfileEditForm(request.POST or None, request.FILES or None, instance=user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Профиль обновлён.')
        return redirect('users:profile', pk=user.pk)
    return render(request, 'users/profile_edit.html', {'form': form, 'profile_user': user})


def user_list(request):
    users = User.objects.all()
    active_filter = request.GET.get('filter', '')

    if request.user.is_authenticated and active_filter:
        if active_filter == 'favorite_authors':
            users = users.filter(
                authored_projects__favorited_by=request.user
            ).distinct()
        elif active_filter == 'participating':
            users = users.filter(
                authored_projects__participants=request.user
            ).exclude(pk=request.user.pk).distinct()
        elif active_filter == 'liked_my':
            users = users.filter(
                favorite_projects__author=request.user
            ).distinct()
        elif active_filter == 'my_members':
            users = users.filter(
                joined_projects__author=request.user
            ).exclude(pk=request.user.pk).distinct()

    paginator = Paginator(users, 12)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'users/user_list.html', {
        'page_obj': page,
        'active_filter': active_filter,
    })


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('projects:list')

    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно изменён.')
        return super().form_valid(form)
