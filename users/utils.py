import json

from orders.models import Order, OrderItem
from products.models import Product
from projects.models import Project
from users.models import Customer


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_subtotal': 0, 'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            if product.discount_price:
                total = (int(product.discount_price) * int(cart[i]['quantity']))
                pprice = int(product.discount_price)
            else:
                total = (int(product.price) * int(cart[i]['quantity']))
                pprice = int(product.price)

            order['get_cart_subtotal'] += int(total)
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'foto1': product.foto1,
                    'name': product.name,
                    'presenta': product.presenta,
                    'price': pprice,
                    'costo': product.costo,
                    },
                'quantity': cart[i]['quantity'],
                'digital':product.digital,
                'get_total': total,
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    order['get_cart_total'] += order['get_cart_subtotal'] + 7000

    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    return {'cartItems': cartItems, 'order': order, 'items': items}


def gestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']
    cookieData = cookieCart(request)
    items = cookieData['items']
    customer, created = Customer.objects.get_or_create(
        email=email,
        )
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False,)

    for item in items:
        product = Product.objects.get(id=item['product']["id"])
        orderItem = OrderItem.objects.create(product=product, order=order, quantity=item['quantity'])

    return customer, order

