from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import CreateUserForm, CustomerForm, ReactivateUser
from .models import User, Customer, Estilo
from .utils import cartData


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        users = User.objects.all()
        regEmail = request.POST.get('email')
        us_reg = users.filter(email=regEmail)

        for user in users:
            if regEmail == user.email:
                if user.is_active == False:
                    cartItems = 0
                    messages.success(request, 'El correo ingresado ya existia pero la cuenta fue suspendida')
                    return redirect('reactivate_user')
                else:
                    messages.error(request, 'El correo ingresado ya existe')
                    return redirect('login')

            if not us_reg:
                form = CreateUserForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    username = form.cleaned_data.get('username')
                    group = Group.objects.get(name='customer')
                    user.groups.add(group)
                    Customer.objects.create(
                        user=user,
                        name=username,
                        email=user.email,
                        )
                    messages.success(request, 'La cuenta de ' + username + ' fue creada satisfactoriamente')
                    return redirect('login')

        form = {}
        messages.info(request, 'Algo no salio bien, Intentalo de nuevo')
        return redirect('register')

    context = {'form': form}
    return render(request, 'users/logs/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Algo no salio bien, Intentalo de nuevo')

    # index del canasto
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
    else:
        cartItems = 0

    context = {'cartItems': cartItems}
    return render(request, 'users/logs/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

    return render(request, 'users/logs/login.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def userUpdate(request):
    user = request.user.customer
    form = CustomerForm(instance=user)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_page')

    # index del canasto
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems, 'form': form}
    return render(request, 'users/user_update.html', context)


@login_required(login_url='login')
def deleteUser(request, pk):
    user = User.objects.get(id=pk)
    orders = request.user.customer.order_set.all()

    if request.method == 'POST':
        apro_orders = orders.filter(status='En Aprobación')
        if apro_orders:
            for obj in apro_orders:
                obj.delete()

        user = request.user
        user.is_active = False
        user.save()
        logout(request)
        messages.success(request, 'Tu cuenta ya esta suspendida.')
        return redirect('home')

    return render(request, 'users/delete_user.html')


def reactivateUser(request):
    form = ReactivateUser(request.POST)
    if request.method == "POST":
        users = User.objects.all()
        regEmail = request.POST.get('email')
        user = users.filter(email=regEmail)
        for user in users:
            if regEmail == user.email:
                if form.is_valid():
                    user.is_active = True
                    user.save()
                    messages.success(request, 'La cuenta de ' + regEmail + ' fue reactivada satisfactoriamente')
                    return redirect('login')

    context = {'form':form}
    return render(request, 'users/logs/reactivateUser.html', context)


# USERS
@login_required(login_url='login')
def userPage(request):
    user = request.user.customer.id
    customer = request.user.customer

    if customer.estilo == 'accounts.Estilo.None':
        estilo = Estilo.objects.get(customer=str(user))

    orders = request.user.customer.order_set.all()
    payment_orders = orders.filter(status='En Aprobación', complete=True)
    payment_done = orders.filter(status='Pago Realizado')
    pending_orders = orders.filter(status='Pendiente')
    indelivery_orders = orders.filter(status='En Ruta')
    delivered_orders = orders.filter(status='Entregado')
    rejected_orders = orders.filter(status='Rechazado')

    total_orders = orders.count()
    payment = orders.filter(status='En Aprobación', complete=True).count()
    pay = payment_done.filter(status='Pago Realizado').count()
    pending = orders.filter(status='Pendiente').count()
    indelivery = orders.filter(status='En Ruta').count()
    delivered = orders.filter(status='Entregado').count()
    rejected = orders.filter(status='Rechazado').count()

    # index del canasto
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems, 'orders': orders, 'total_orders': total_orders,
        'payment_orders': payment_orders, 'payment_done': payment_done, 'pending_orders': pending_orders, 
        'indelivery_orders': indelivery_orders, 'delivered_orders': delivered_orders, 'rejected_orders': rejected_orders, 
        'payment': payment, 'pay': pay, 'pending': pending, 'indelivery': indelivery, 'delivered': delivered, 'rejected': rejected,}
    return render(request, 'users/user.html', context)

