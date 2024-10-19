from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Carrito, CarritoProducto
import mercadopago
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.template import RequestContext

def carrito(request):
    return HttpResponse("Esta es la página del carrito de compras.")

def menu_html(request):
    return render(request, 'tienda/menu.html')

def home(request):
     return render(request, 'tienda/home.html')

def iniciar_sesion(request):
    if request.method == 'POST':
        email = request.POST['login-email']
        password = request.POST['login-password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu')
        else:
            error = "El correo electrónico o la contraseña son incorrectos."
            return render(request, 'home.html', {'error': error})
    else:
        return render(request, 'home.html')


def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/lista_productos.html', {'productos': productos})

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, _ = Carrito.objects.get_or_create(id=request.session.get('carrito_id', None))
    CarritoProducto.objects.create(carrito=carrito, producto=producto, cantidad=1)
    request.session['carrito_id'] = carrito.id
    return redirect('lista_productos')

def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(id=request.session.get('carrito_id', None))
    productos_en_carrito = CarritoProducto.objects.filter(carrito=carrito)
    total = sum(item.producto.precio * item.cantidad for item in productos_en_carrito)
    return render(request, 'tienda/ver_carrito.html', {'carrito': carrito, 'total': total})


def pagar(request):
    if request.method == 'POST':
        sdk = mercadopago.SDK("YOUR_ACCESS_TOKEN")
        carrito, _ = Carrito.objects.get_or_create(id=request.session.get('carrito_id', None))
        total = sum(item.producto.precio * item.cantidad for item in carrito.carritoproducto_set.all())
        preference_data = {
            "items": [
                {
                    "title": "Compra en Choco's Treats",
                    "quantity": 1,
                    "currency_id": "USD",
                    "unit_price": float(total)
                }
            ]
        }
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        return redirect(preference["init_point"])
    return render(request, 'tienda/pagar.html')
