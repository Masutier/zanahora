from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from users.decorators import unauthenticated_user, allowed_users, admin_only
from .models import Coupon
from .forms import CreateCouponForm

import json


@csrf_exempt
def validate_cupon(request):
    """
        Verifica el cupon y devuelve el descuento que posee
    """
    if request.method == 'GET':
        coupon = request.GET.get('coupon', None)
        if coupon:
            data = get_object_or_404(Coupon, code=coupon)
            data1 = Coupon.objects.get(code='CINCO')
            if data.active:
                return JsonResponse({
                    "discount": data.discount
                })
            else:
                raise Http404


def Cupones(request):
    cupones = Coupon.objects.all()

    context = {'title': "Cupones", 'cupones': cupones}
    return render(request, 'cupons/coupons.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createCupon (request):
    cuponForm = CreateCouponForm()

    if request.method == 'POST':
        cuponForm = CreateCouponForm(request.POST, request.FILES)
        if cuponForm.is_valid():
            cuponForm.save()
            return redirect('adminHome')

    context = {"title": "Crear Cupon", "cuponForm": cuponForm}
    return render(request, 'cupons/createCupon.html', context)
