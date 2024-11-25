from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Portfolio, Project
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import UserProfileForm, PortfolioForm, ProjectForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('create_profile')
    else:
        form = UserCreationForm()
    return render(request, 'portfolio/register.html', {'form': form})

@login_required
def create_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'portfolio/create_profile.html', {'form': form})

@login_required
def view_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'portfolio/view_profile.html', {'profile': profile})

@login_required
def edit_portfolio(request):
    try:
        portfolio = request.user.portfolio
    except Portfolio.DoesNotExist:
        portfolio = Portfolio(user=request.user)

    if request.method == 'POST':
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            form.save()
            return redirect('view_portfolio')
    else:
        form = PortfolioForm(instance=portfolio)

    return render(request, 'portfolio/edit_portfolio.html', {'form': form})

@login_required
def view_portfolio(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    projects = portfolio.projects.all()
    return render(request, 'portfolio/view_portfolio.html', {'portfolio': portfolio, 'projects': projects})

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.portfolio = request.user.portfolio
            project.save()
            return redirect('view_portfolio')
    else:
        form = ProjectForm()

    return render(request, 'portfolio/add_project.html', {'form': form})

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, portfolio__user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('view_portfolio')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'portfolio/edit_project.html', {'form': form, 'project': project})

