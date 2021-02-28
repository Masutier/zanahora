import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from xhtml2pdf import pisa

from users.decorators import unauthenticated_user, allowed_users, admin_only

from orders.forms import OrderForm

from orders.models import Order
from products.models import Product, Estilo
from projects.models import Project
from users.models import Customer

from .utils import render_to_pdf
from products.utils import category, Natural
from projects.utils import project
from users.utils import cartData


@login_required(login_url='login')
@admin_only
def adminHome(request):
    customers = Customer.objects.all()
    total_customers = customers.count()
    orders_all = Order.objects.all()
    products = Product.objects.all()
    projects = Project.objects.all()

    # orders
    payment_orders = orders_all.filter(status='En Aprobación', complete=True)
    payment_done = orders_all.filter(status='Pago Realizado')
    pending_orders = orders_all.filter(status='Pendiente')
    indelivery_orders = orders_all.filter(status='En Ruta')
    deliver_conf_orders = orders_all.filter(status='Entrega Confirmada')
    delivered_orders = orders_all.filter(status='Entregado')
    rejected_orders = orders_all.filter(status='Rechazado')

    total_orders = orders_all.count()
    payment = payment_orders.count()
    pay = payment_done.count()
    pending = pending_orders.count()
    indelivery = indelivery_orders.count()
    indelconf = deliver_conf_orders.count()
    delivered = delivered_orders.count()
    rejected = rejected_orders.count()

    orders = []
    ordEstado = []
    for obj in orders_all:
        if obj.transaction_id:
            orders.append(obj)
    # categorias
        if obj.status not in ordEstado:
            ordEstado.append(obj.status)

    # products
    apply_products = products.filter(status='Apply')
    aproved_products = products.filter(status='Aproved')
    void_products = products.filter(status='Void')
    deleted_products = products.filter(status='Delete')

    total_products = products.count()
    apply = apply_products.count()
    aproved = aproved_products.count()
    void = void_products.count()
    delete = deleted_products.count()

    prodEstado = []
    for obj in products:
        if obj.status not in prodEstado:
            prodEstado.append(obj.status)

    # categorias
    categ = category(request)
    categorias = categ['categorias']
    # prodyectos
    proye = project(request)
    projectos = proye['projectos']
    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {
        'orders': orders,
        'total_orders': total_orders, 'ordEstado': ordEstado, 'prodEstado': prodEstado,
        'payment_orders': payment_orders, 'payment_done': payment_done, 'pending_orders': pending_orders, 'indelivery_orders': indelivery_orders,
        'deliver_conf_orders': deliver_conf_orders, 'delivered_orders': delivered_orders, 'rejected_orders': rejected_orders,
        'payment': payment, 'pay': pay, 'pending': pending, 'indelivery': indelivery, 'indelconf':indelconf, 'delivered': delivered, 'rejected': rejected,
        'products': products,
        'total_products': total_products,
        'apply_products': apply_products, 'aproved_products': aproved_products, 'void_products': void_products,
        'deleted_products': deleted_products,
        'apply': apply, 'aproved': aproved, 'void': void, 'delete': delete,
        'projectos': projectos, 
        'customers': customers, 'total_customers': total_customers, 'cartItems': cartItems}
    return render(request, 'mainAdmin/dashboard/dashboard.html', context)


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
    return render(request, 'mainAdmin/products/products_project.html', context)


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
    return render(request, 'mainAdmin/products/prod_invent.html', context)






# ORDERS

@login_required(login_url='login')
@admin_only
def orders(request):
    products = Product.objects.all()
    orders_all = Order.objects.all()
    total_orders = orders_all.count()

    # orders
    payment_orders = orders_all.filter(status='En Aprobación', complete=True)
    payment = payment_orders.count()
    payment_done = orders_all.filter(status='Pago Realizado')
    pay = payment_done.count()
    pending_orders = orders_all.filter(status='Pendiente')
    pending = pending_orders.count()
    indelivery_orders = orders_all.filter(status='En Ruta')
    indelivery = indelivery_orders.count()
    indelconf_orders = orders_all.filter(status='Entrega Confirmada')
    indelconf = indelconf_orders.count()
    delivered_orders = orders_all.filter(status='Entregado')
    delivered = delivered_orders.count()
    rejected_orders = orders_all.filter(status='Rechazado')
    rejected = rejected_orders.count()

    orders = []
    ordEstado = []
    for obj in orders_all:
        if obj.transaction_id:
            orders.append(obj)
    # categorias
        if obj.status not in ordEstado:
            ordEstado.append(obj.status)
    
    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'orders': orders, 'cartItems': cartItems, 'products': products, 'ordEstado': ordEstado,
        'total_orders': total_orders, 
        'payment_orders': payment_orders, 'payment_done': payment_done, 'pending_orders': pending_orders, 'indelivery_orders': indelivery_orders,
        'indelconf_orders': indelconf_orders, 'delivered_orders': delivered_orders, 'rejected_orders': rejected_orders,
        'payment': payment, 'pay': pay, 'pending': pending, 'indelivery': indelivery, 'indelconf': indelconf, 'delivered': delivered, 'rejected': rejected,}
    return render(request, 'mainAdmin/orders/orders.html', context)


@login_required(login_url='login')
@admin_only
def ordersDetailToAprove(request):
    orders_all = Order.objects.all()
    ordTitle = "En Aprobación"
    ordersDetail = orders_all.filter(status='En Aprobación', complete=True)
    orderCount = ordersDetail.count()
    
    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'cartItems': cartItems, 'ordTitle': ordTitle, 'ordersDetail': ordersDetail, 'orderCount': orderCount}
    return render(request, 'mainAdmin/orders/orders_detail.html', context)


@login_required(login_url='login')
@admin_only
def ordersDetailConfirm(request):
    orders_all = Order.objects.all()
    ordTitle = "Pago Realizado"
    ordersDetail = orders_all.filter(status='Pago Realizado')
    orderCount = ordersDetail.count()
    
    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'cartItems': cartItems, 'ordTitle': ordTitle, 'ordersDetail': ordersDetail, 'orderCount': orderCount}
    return render(request, 'mainAdmin/orders/orders_detail.html', context)


@login_required(login_url='login')
@admin_only
def ordersDetailPending(request):
    orders_all = Order.objects.all()
    ordTitle = "Pendientes"
    ordersDetail = orders_all.filter(status='Pendiente')
    orderCount = ordersDetail.count()
    
    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'cartItems': cartItems, 'ordTitle': ordTitle, 'ordersDetail': ordersDetail, 'orderCount': orderCount}
    return render(request, 'mainAdmin/orders/orders_detail.html', context)


@login_required(login_url='login')
@admin_only
def ordersDetailRuta(request):
    orders_all = Order.objects.all()
    ordTitle = "En Ruta"
    ordersDetail = orders_all.filter(status='En Ruta')
    orderCount = ordersDetail.count()

    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'cartItems': cartItems, 'ordTitle': ordTitle, 'ordersDetail': ordersDetail, 'orderCount': orderCount}
    return render(request, 'mainAdmin/orders/orders_detail.html', context)


@login_required(login_url='login')
@admin_only
def ordersDetailDelivConfRuta(request):
    orders_all = Order.objects.all()
    ordTitle = "Entrega Confirmada"
    ordersDetail = orders_all.filter(status='Entrega Confirmada')
    orderCount = ordersDetail.count()

    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'cartItems': cartItems, 'ordTitle': ordTitle, 'ordersDetail': ordersDetail, 'orderCount': orderCount}
    return render(request, 'mainAdmin/orders/orders_detail.html', context)


@login_required(login_url='login')
@admin_only
def ordersDetailDelivered(request):
    orders_all = Order.objects.all()
    ordTitle = "Entregadas"
    ordersDetail = orders_all.filter(status='Entregado')
    orderCount = ordersDetail.count()

    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'cartItems': cartItems, 'ordTitle': ordTitle, 'ordersDetail': ordersDetail, 'orderCount': orderCount}
    return render(request, 'mainAdmin/orders/orders_detail.html', context)


@login_required(login_url='login')
@admin_only
def ordersDetailReject(request):
    orders_all = Order.objects.all()
    ordTitle = "Rechazadas"
    ordersDetail = orders_all.filter(status='Rechazado')
    orderCount = ordersDetail.count()

    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'cartItems': cartItems, 'ordTitle': ordTitle, 'ordersDetail': ordersDetail, 'orderCount': orderCount}
    return render(request, 'mainAdmin/orders/orders_detail.html', context)


@login_required(login_url='login')
@admin_only
def ordersDeepSearch(request):
    orders_all = Order.objects.all()
    payment_orders = orders_all.filter(status='En Aprobación', complete=False)
    payment = payment_orders.count()

    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'cartItems': cartItems, 'payment_orders': payment_orders, 'payment': payment}
    return render(request, 'mainAdmin/orders/orders_deep.html', context)









# PDF
@login_required(login_url='login')
def ocRepartoPDF(request, pk):
    products = Product.objects.all()

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('admin_home')

    context = {'form': form, 'order':order, 'products': products}

    pdf = render_to_pdf('mainAdmin/pdf/oc_reparto_PDF.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


@login_required(login_url='login')
def ocRepartoDownloadPDF(request, pk):
    products = Product.objects.all()

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('admin_home')

    context = {'form': form, 'order':order, 'products': products}

    pdf = render_to_pdf('mainAdmin/pdf/oc_reparto_PDF.html', context)

    response = HttpResponse(pdf, content_type='application/pdf')
    filename = 'ZanaHora_Orden:%s.pdf' %(order.id)
    content = "attachment; filename='%s'" %(filename)
    response['Content-Disposition'] = content
    return response


@login_required(login_url='login')
@admin_only
def ordenCompraPDF(request):
    products = Product.objects.all()
    orders_all = Order.objects.all()

    pending_orders = orders_all.filter(status='Pendiente')
    pending = pending_orders.count()

    proyectos = []
    for product in products:
        if product.proyect not in proyectos:
            proyectos.append(product.proyect)

    context = {'pending': pending, 'pending_orders': pending_orders, 'proyectos': proyectos, 'products': products,}

    pdf = render_to_pdf('mainAdmin/pdf/oc_all_PDF.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


@login_required(login_url='login')
@admin_only
def ordenCompraDownloadPDF(request):
    x = datetime.datetime.now()
    products = Product.objects.all()
    orders_all = Order.objects.all()

    pending_orders = orders_all.filter(status='Pendiente')
    pending = pending_orders.count()

    proyectos = []
    for product in products:
        if product.proyect not in proyectos:
            proyectos.append(product.proyect)

    context = {'pending': pending, 'pending_orders': pending_orders, 'proyectos': proyectos, 'products': products,}

    pdf = render_to_pdf('mainAdmin/pdf/oc_all_PDF.html', context)

    response = HttpResponse(pdf, content_type='application/pdf')
    filename = 'OC_all_%s.pdf' %x
    content = "attachment; filename='%s'" %(filename)
    response['Content-Disposition'] = content
    return response