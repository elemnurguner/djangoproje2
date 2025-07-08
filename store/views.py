from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderItem
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})



def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'store/product_list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'store/product_detail.html', {'product': product})


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.error(request, "Sepete ürün eklemek için giriş yapmalısınız.")
        return redirect('users:login')
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1  # Aynı üründen varsa miktarı artır
    else:
        cart[str(product_id)] = 1  # Yoksa ekle

    request.session['cart'] = cart
    return redirect('store:cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    
    cart_items = []
    total_price = 0
    for product in products:
        quantity = cart.get(str(product.id), 0)
        subtotal = product.price * quantity
        total_price += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'store/cart_detail.html', context)

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('store:cart_detail')

def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            cart.pop(str(product_id), None)
        request.session['cart'] = cart
    return redirect('store:cart_detail')

def checkout(request):
    if not request.user.is_authenticated:
        messages.error(request, "Sipariş vermek için giriş yapmalısınız.")
        return redirect('users:login')
    
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('store:cart_detail')

    total_price = 0
    order_items = []

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        if product.stock < quantity:
            # Stok yetmiyor
            return render(request, 'store/checkout_error.html', {'message': f"Stok yetersiz: {product.name}"})
        total_price += product.price * quantity
        order_items.append((product, quantity))

    # Stok düşür ve Order kaydet
    order = Order.objects.create(user=request.user, total_price=total_price)

    for product, quantity in order_items:
        product.stock -= quantity
        product.save()
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

    # Sepeti temizle
    request.session['cart'] = {}

    return render(request, 'store/checkout_success.html', {'order': order})