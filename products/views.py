import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from users.decorators import unauthenticated_user, allowed_users, admin_only

from .forms import CreateProductForm

from .models import Product, Estilo, Natural
from projects.models import Project

from .utils import category
from projects.utils import project
from users.utils import cartData


def prodAll(request):
    projects = Project.objects.all()
    products_all = Product.objects.all()

    # search
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        prod=Product.objects.filter(name__istartswith = search_str)
        data = prod.values()
        return JsonResponse(list(data), safe=False)
    
    # productos a mostrar
    products = []
    for product in products_all:
        if product.status == 'Aproved':
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
    
    context = {'cartItems': cartItems, 'products': products, "categorias": categorias, 'projectos': projectos, 'natural': natural, 'estilo': estilo}
    return render(request, 'products/prod_all.html', context)


def product_detail(request, id):
    obj = get_object_or_404(Product, id=id)
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

    context = {'cartItems': cartItems, 'object': obj, 'categorias': categorias, 'natural': natural}
    return render(request, "products/product_detail.html", context)


def prod_by_category(request, obj):
    products = Product.objects.filter(categoria=obj, status='Aproved')
    totalProducts = Product.objects.filter(categoria=obj, status='Aproved').count()

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

    context = {'cartItems': cartItems, "products": products, 'projectos': projectos, 'obj': obj, 'categorias': categorias,
     'natural': natural, "estilo": estilo, 'page_range1': page_range1, 'totalProducts': totalProducts}
    return render(request, 'products/prod_by_category.html', context)


def product_offert(request):
    projects = Project.objects.all()
    products = Product.objects.filter(label='Oferta', status='Aproved')
    totalProducts = Product.objects.filter(label='Oferta', status='Aproved').count()
    prodTitle = "Lista de Productos En Oferta"

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

    context = {'cartItems': cartItems, "products": products, 'projectos': projectos, 'categorias': categorias,
     'natural': natural, 'estilo': estilo, 'page_range1': page_range1, 'totalProducts': totalProducts, 'prodTitle': prodTitle}
    return render(request, 'products/prod_estilo.html', context)


def product_special(request):
    projects = Project.objects.all()
    products = Product.objects.filter(label='Especial', status='Aproved')
    totalProducts = Product.objects.filter(label='Especial', status='Aproved').count()
    prodTitle = "Lista de Productos Especiales"

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

    context = {'cartItems': cartItems, "products": products, 'projectos': projectos, 'categorias': categorias,
     'natural': natural, 'estilo': estilo, 'page_range1': page_range1, 'totalProducts': totalProducts, 'prodTitle': prodTitle}
    return render(request, 'products/prod_estilo.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createProduct(request):
    productForm = CreateProductForm()

    if request.method == 'POST':
        productForm = CreateProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
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

    context = {'productForm': productForm, 'cartItems': cartItems, 'products': products, "categorias": categorias, 'projectos': projectos,
     'natural': natural, 'estilo': estilo}
    return render(request, 'products/logs/create_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    productForm = CreateProductForm(instance=product)
    if request.method == 'POST':
        productForm = CreateProductForm(request.POST, request.FILES, instance=product)
        if productForm.is_valid():
            productForm.save()
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

    context = {'productForm': productForm, 'cartItems': cartItems,
     'natural': natural, 'estilo': estilo}
    return render(request, 'products/logs/update_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def fastUpdateProduct(request, pk):
    product = Product.objects.get(id=pk)
    productForm = CreateProductForm(instance=product)
    if request.method == 'POST':
        productForm = CreateProductForm(request.POST, request.FILES, instance=product)
        if productForm.is_valid():
            productForm.save()
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

    context = {'productForm': productForm, 'product': product, 'cartItems': cartItems,
     'natural': natural, 'estilo': estilo}
    return render(request, 'products/logs/fast_update_prod.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('adminHome')

    context = {'item': product}
    return render(request, 'products/logs/delete_product.html', context)
