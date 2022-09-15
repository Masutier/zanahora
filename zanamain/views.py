from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect

from products.models import Product, Natural
from projects.models import Project
from users.models import Estilo

from products.utils import category
from projects.utils import project
from users.utils import cartData


def home(request):
    projects = Project.objects.all()
    products_all = Product.objects.all()
    totalProducts = Product.objects.all().count()

    # productos a mostrar
    products = []
    for product in products_all:
        if product.status == 'Aproved' and product.cantidad != None:
            products.append(product)

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
    paginator = Paginator(products, 12)
    page = request.GET.get('page1')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    index1 = products.number - 1
    max_index1 = len(paginator.page_range)
    start_index1 = index1 - 3 if index1 >= 3 else 0
    end_index1 = index1 + 3 if index1 <= max_index1 else max_index1
    page_range1 = paginator.page_range[start_index1:end_index1]

    context = {'cartItems': cartItems, 'products': products, 'projectos': projectos, 'categorias': categorias, 'natural': natural, "estilo": estilo,
    'page_range1': page_range1, 'totalProducts': totalProducts}
    return render(request, 'zanamain/zanahora.html', context)


# INFORMACION
def agroecologia (request):
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

    context = {'cartItems': cartItems, 'products': products, 'projectos': projectos, 'categorias': categorias, 'natural': natural, 'estilo': estilo}
    return render(request, 'zanamain/info/info_agroecol.html', context)


def infoEntregas (request):
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

    context = {'cartItems': cartItems, 'products': products, 'projectos': projectos, 'categorias': categorias, 'natural': natural, 'estilo': estilo}
    return render(request, 'zanamain/info/info_entregas.html', context)


def informacionIconos (request):
    projects = Project.objects.all()
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

    context = {'cartItems': cartItems, 'products': products, 'projectos': projectos, 'categorias': categorias, 'natural': natural, 'estilo': estilo}
    return render(request, 'zanamain/info/info_icons.html', context)


def informacionConditions (request):
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

    context = {'cartItems': cartItems, 'products': products, 'projectos': projectos, 'categorias': categorias, 'natural': natural, 'estilo': estilo}
    return render(request, 'zanamain/info/info_conditions.html', context)


def informacionPrivacy (request):
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

    context = {'cartItems': cartItems, 'products': products, 'projectos': projectos, 'categorias': categorias, 'natural': natural, 'estilo': estilo}
    return render(request, 'zanamain/info/info_privacy.html', context)



