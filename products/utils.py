from .models import Product


def category(request):
    products = Product.objects.all()
    # categorias
    categorias = []
    for product in products:
        if product.categoria not in categorias:
            categorias.append(product.categoria)
    
    return {'categorias': categorias}
