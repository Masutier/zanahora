from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect

from products.models import Product, Estilo
from projects.models import Project

from products.utils import category, Natural
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
    return render(request, 'accounts/zanahora.html', context)






# PRODUCTS

@login_required(login_url='login')
@admin_only
def productsCateg(request):
    products = Product.objects.all()

    total_products = products.count()
    apply = products.filter(status='Apply').count()
    aproved = products.filter(status='Aproved').count()
    void = products.filter(status='Void').count()
    delete = products.filter(status='Delete').count()

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
    
    context = {'products': products, "categorias": categorias, 'total_products': total_products,
        'apply': apply, 'aproved': aproved, 'void': void, 'delete': delete,
        'cartItems': cartItems, 'projectos': projectos, 'natural': natural, 'estilo': estilo}
    return render(request, 'mainAdmin/products/products_categ.html', context)


@login_required(login_url='login')
@admin_only
def productsProject(request):
    products = Product.objects.all()

    total_products = products.count()
    apply = products.filter(status='Apply').count()
    aproved = products.filter(status='Aproved').count()
    void = products.filter(status='Void').count()
    delete = products.filter(status='Delete').count()

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
    
    context = {'products': products, "categorias": categorias, 'total_products': total_products,
        'apply': apply, 'aproved': aproved, 'void': void, 'delete': delete,
        'cartItems': cartItems, 'projectos': projectos, 'natural': natural, 'estilo': estilo}
    return render(request, 'administracion/products/products_project.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def inventoryProduct(request):
    products_all = Product.objects.all()

    productAproved = []
    for product in products_all:
        if product.status == 'Aproved' and product.perecedero == False:
            productAproved.append(product)

    prodAproveNoPerece = productAproved
    
    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'cartItems': cartItems, 'prodAproveNoPerece': prodAproveNoPerece,}
    return render(request, 'administracion/products/prod_invent.html', context)
