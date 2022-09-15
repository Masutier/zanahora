from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404

from users.decorators import unauthenticated_user, allowed_users, admin_only

from .forms import CreateProjectForm

from .models import Project, Video
from products.models import Product, Natural
from users.models import Estilo

from .utils import project
from products.utils import category
from users.utils import cartData


def projectsAll(request):
    projects = Project.objects.filter(status='Aproved')
    totalProjects = Project.objects.filter(status='Aproved').count()

    # categorias
    categ = category(request)
    categorias = categ['categorias']
    # prodyectos
    proye = project(request)
    projectos = proye['projectos']
    # natural
    natural = Natural.objects.all()
    # estilo
    estilo = Estilo.objects.all()
    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    # pagination
    paginator = Paginator(projects, 12)
    page = request.GET.get('page1')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    index1 = projects.number - 1
    max_index1 = len(paginator.page_range)
    start_index1 = index1 - 3 if index1 >= 3 else 0
    end_index1 = index1 + 3 if index1 <= max_index1 else max_index1
    page_range1 = paginator.page_range[start_index1:end_index1]

    context = {'cartItems': cartItems, "projects": projects, 'projectos': projectos, 'categorias': categorias,
    'natural': natural, 'estilo': estilo, 'page_range1': page_range1, 'totalProjects': totalProjects}
    return render(request, 'projects/projects_all.html', context)


def project_detail(request, id):
    obj = get_object_or_404(Project, id=id)
    videos = Video.objects.filter(project=id)
    products_all = Product.objects.all()
    products = products_all.filter(project=id)

    # categorias
    categ = category(request)
    categorias = categ['categorias']
    # prodyectos
    proye = project(request)
    projectos = proye['projectos']
    # natural
    natural = Natural.objects.all()
    # estilo
    estilo = Estilo.objects.all()
    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'cartItems': cartItems, 'object': obj, 'videos': videos, 'products': products, 'categorias': categorias, 'natural': natural}
    return render(request, "projects/project_detail.html", context)


@login_required(login_url='login')
@admin_only
def projects(request):
    projects = Project.objects.all()

    total_projects = projects.count()
    apply = projects.filter(status='Apply').count()
    aproved = projects.filter(status='Aproved').count()
    void = projects.filter(status='Void').count()
    delete = projects.filter(status='Delete').count()

    # categorias
    categ = category(request)
    categorias = categ['categorias']
    # prodyectos
    proye = project(request)
    projectos = proye['projectos']
    # natural
    natural = Natural.objects.all()
    # estilo
    estilo = Estilo.objects.all()
    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0
    
    context = {'projects': projects, "categorias": categorias, 'total_projects': total_projects,
        'apply': apply, 'aproved': aproved, 'void': void, 'delete': delete,
        'cartItems': cartItems, 'projectos': projectos, 'natural': natural, 'estilo': estilo}
    return render(request, 'mainAdmin/projects/projects.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createProject(request):
    projectForm = CreateProjectForm()

    if request.method == 'POST':
        projectForm = CreateProjectForm(request.POST, request.FILES)
        if projectForm.is_valid():
            projectForm.save()
            return redirect('adminHome')

    products = Product.objects.all()

    # categorias
    categ = category(request)
    categorias = categ['categorias']
    # prodyectos
    proye = project(request)
    projectos = proye['projectos']
    # natural
    natural = Natural.objects.all()
    # estilo
    estilo = Estilo.objects.all()
    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'projectForm': projectForm, 'cartItems': cartItems, 'products': products, "categorias": categorias, 'projectos': projectos,
     'natural': natural, 'estilo': estilo}
    return render(request, 'projects/logs/create_project.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    projectForm = CreateProjectForm(instance=project)
    if request.method == 'POST':
        projectForm = CreateProjectForm(request.POST, request.FILES, instance=project)
        if projectForm.is_valid():
            projectForm.save()
            return redirect('adminHome')

    # natural
    natural = Natural.objects.all()
    # estilo
    estilo = Estilo.objects.all()
    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'projectForm': projectForm, 'cartItems': cartItems,
     'natural': natural, 'estilo': estilo}
    return render(request, 'projects/logs/update_project.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('adminHome')

    context = {'item': project}
    return render(request, 'projects/logs/delete_project.html', context)
