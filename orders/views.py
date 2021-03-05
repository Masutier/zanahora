import json
import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from users.decorators import unauthenticated_user, allowed_users, admin_only

from .forms import OrderForm, OrderFormStat

from .models import Order, OrderItem
from products.models import Product, Estilo, Natural
from projects.models import Project

from products.utils import category
from projects.utils import project
from users.utils import cartData


@login_required(login_url='login')
def cart(request):
    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
    else:
        cartItems = 0
        order = []
        items = []

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'orders/cart/cart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)

    if product.discount_price:
        itemPrice = int(product.discount_price)
    else:
        itemPrice = int(product.price)

    itemCosto = int(product.costo)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, itemPrice=itemPrice, itemCosto=itemCosto)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
        messages.success(request, 'Item se adiciono al canasto')
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        messages.success(request, 'Item se removió del canasto')

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@login_required(login_url='login')
def checkout(request, order_id=None):
    # index del canasto
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'orders/cart/checkout.html', context)


@login_required(login_url='login')
def get_checkout_items(request, order_id=None):
    if request.method == 'GET':
        # query = get_object_or_404(Order, id=order_id)
        # items = query.orderitem_set.all()
        data = cartData(request)
        item = data['items']
        items = []
        for i in item:
            x = json.dumps({
                'name': i.product.name,
                'presentation': i.product.presenta,
                'quantity': i.quantity,
                'price': int(i.product.discount_price)* i.quantity if i.product.discount_price else int(i.product.price)* i.quantity,
            })
            items.append(x)
        return JsonResponse({
            'items': items
        })


# ORDERS
@login_required(login_url='login')
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    total = data['form']['total']
    addressUse = data['addressUse']
    order.transaction_id = transaction_id

    if int(total) == int(order.get_cart_total):
        order.complete = True
    
    if order.shipping == True:
        if addressUse == 'myAddress':
            order.address = customer.address
            order.barrio = customer.barrio
            order.city = customer.city
            order.state = customer.state
            order.country = customer.country
            order.zipcode = customer.zipcode

        if addressUse == 'otrAddress':
            order.address = data['shipping']['address']
            order.barrio = data['shipping']['barrio'],
            order.city = data['shipping']['city'],
            order.state = data['shipping']['state'],
            order.country = data['shipping']['country'],
            order.zipcode = data['shipping']['zipcode'],

    order.save()

    # EMAIL
    subject = 'Gracias por tu compra, Opciones de Pago para tu orden #' + str(order.id)
    html_message = render_to_string(
        'orders/mail/payment_option_mail.html',
        context={
           "name": order.customer.name,
           "total": total,
           "orden": order.id
        }
    )
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = [order.customer.email]
    mail.send_mail(subject, plain_message, from_email, to, html_message=html_message)

    return JsonResponse('Tu pedido ya entro para ser procesado, Gracias',  safe=False)


@login_required(login_url='login')
def orderDetail(request, pk):
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get(id=pk)
        items = order.orderitem_set.all()

    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'orders/order_detail.html', context)


@login_required(login_url='login')
def confirmaPago(request, pk):
    customer = request.user.customer
    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            order.status = "Pago Realizado"
            order.save()
            return redirect('user_page')

    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'form': form, 'order': order, 'cartItems': cartItems}
    return render(request, 'orders/pay_confirm.html', context)


@login_required(login_url='login')
def updateOrder(request, pk):
    products = Product.objects.all()

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('adminHome')
        else:
            messages.info(request, 'Algo no salio bien, Revisa bien la información ingresada')

    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'form': form, 'order': order, 'products': products, 'cartItems':cartItems}
    return render(request, 'orders/update_order.html', context)


@login_required(login_url='login')
def updateOrderStat(request, pk):
    products = Product.objects.all()
    order = Order.objects.get(id=pk)
    stat = order.status
    form = OrderFormStat(instance=order)
    if request.method == 'POST':
        form = OrderFormStat(request.POST, instance=order)
        if form.is_valid():

            if stat == 'En Aprobación' or stat == 'Pago Realizado' and order.status == 'Pendiente':
                for item in order.orderitem_set.all():
                    item.product.cantidad = item.product.cantidad - item.quantity
                    obj = Product.objects.get(name=item.product.name)
                    obj.cantidad = item.product.cantidad
                    obj.save()
                messages.info(request, 'Pendiente -- ítems de db')
                form.save()
                return redirect('adminHome')

            if stat == 'En Aprobación' or stat == 'Pago Realizado' and order.status == 'Entregado':
                for item in order.orderitem_set.all():
                    item.product.cantidad = item.product.cantidad - item.quantity
                    obj = Product.objects.get(name=item.product.name)
                    obj.cantidad = item.product.cantidad
                    obj.save()
                messages.info(request, 'Entregado -- ítems de db')
                form.save()
                return redirect('adminHome')

            if stat == 'En Aprobación' or stat == 'Pago Realizado' and order.status == 'Rechazado':
                messages.info(request, '==> Rechazado No db')
                form.save()
                return redirect('adminHome')

            if stat == 'Pendiente' or stat == 'En Ruta' or stat == 'Entrega Confirmada' and order.status == 'Entregado':
                messages.info(request, '==> Entregado No db')
                form.save()
                return redirect('adminHome')

            if stat == 'Pendiente' and order.status == 'En Aprobación' or order.status == 'Pago Realizado':
                for item in order.orderitem_set.all():
                    item.product.cantidad = item.product.cantidad + item.quantity
                    obj = Product.objects.get(name=item.product.name)
                    obj.cantidad = item.product.cantidad
                    obj.save()
                messages.info(request, 'Pendiente ==> ' + order.status + ' + ítems a db')
                form.save()
                return redirect('adminHome')

            if stat == 'Pendiente' and order.status == 'En Ruta':
                messages.info(request, 'Pendiente ==> ' + order.status + ' No db')
                form.save()
                # EMAIL
                subject = 'Tu orden #' + str(order.id) + 'ya esta en ruta'
                html_message = render_to_string(
                    'orders/mail/order_en_ruta_mail.html',
                    context={
                    "name": order.customer.name,
                    "orden": order.id,
                    "Repartidor1": order.repartidor.name,
                    "Repartidor2": order.repartidor.last_name,
                    "tydoc": order.repartidor.tydoc,
                    "cedulaId": order.repartidor.cedulaId,
                    }
                )
                plain_message = strip_tags(html_message)
                from_email = settings.EMAIL_HOST_USER
                to = [order.customer.email]
                mail.send_mail(subject, plain_message, from_email, to, html_message=html_message)
                return redirect('adminHome')

            if stat == 'En Ruta' and order.status == 'Entrega Confirmada' or order.status == 'Entregado':
                messages.info(request, '==> Entrega Confirmada No db')
                form.save()
                return redirect('adminHome')

            if stat == 'En Ruta' and order.status == 'Pendiente':
                messages.info(request, 'En Ruta ==> ' + order.status + ' No db')
                form.save()
                return redirect('adminHome')

            if stat == 'En Ruta' and order.status == 'Rechazado':
                for item in order.orderitem_set.all():
                    item.product.cantidad = item.product.cantidad + item.quantity
                    obj = Product.objects.get(name=item.product.name)
                    obj.cantidad = item.product.cantidad
                    obj.save()
                messages.info(request, 'Rechazada + ítems a db')
                form.save()
                return redirect('adminHome')

            if stat == 'Entrega Confirmada' and order.status == 'En Ruta' or order.status == 'Pendiente':
                messages.info(request, 'Entrega Confirmada ==> ' + order.status + ' No db')
                form.save()
                return redirect('adminHome')

            messages.info(request, 'La Orden NO se actualizo y no se cambio el estatus')
            return redirect('adminHome')
        else:
            messages.info(request, 'Algo no salio bien, Revisa bien la información ingresada')

    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'form': form, 'order': order, 'products': products, 'cartItems':cartItems}
    return render(request, 'orders/update_order_stat.html', context)



@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('adminHome')

    context = {'item': order}
    return render(request, 'orders/delete_order.html', context)


@login_required(login_url='login')
def userDelOrd(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('user_page')

    context = {'item': order}
    return render(request, 'orders/user_del_ord.html', context)


@login_required(login_url='login')
@admin_only
def simpleOrders(request):
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
    return render(request, 'mainAdmin/orders/orders_simple.html', context)



# ORDERS ADMIN

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


@login_required(login_url='login')
def confirmaEntrega(request, pk):
    customer = request.user.customer
    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            order.status = "Entrega Confirmada"
            order.save()
            return redirect('rep_user_ordens_assign')

    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'form': form, 'order': order, 'cartItems': cartItems}
    return render(request, 'orders/delivery_confirm.html', context)
