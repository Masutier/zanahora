from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from cupons.models import Coupon
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


