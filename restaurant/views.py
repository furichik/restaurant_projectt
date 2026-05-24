from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Dish
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def menu(request):
    categories = Category.objects.all()
    return render(request, 'menu.html', {'categories': categories})


def add_to_cart(request, dish_id):
    if request.method != 'POST':
        return redirect('menu')

    cart = request.session.get('cart', {})
    dish_id = str(dish_id)

    removed_ingredients = request.POST.getlist('remove_ingredients')

    key = dish_id + "_" + "_".join(removed_ingredients)

    if key in cart:
        cart[key]['quantity'] += 1
    else:
        cart[key] = {
            'quantity': 1,
            'removed': removed_ingredients
        }

    request.session['cart'] = cart
    return redirect('menu')


def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for key, item in cart.items():
        dish_id = key.split("_")[0]
        dish = get_object_or_404(Dish, id=dish_id)

        removed = item['removed']
        quantity = item['quantity']

        removed_ingredients = dish.ingredients.filter(name__in=removed)

        removed_price = sum(i.price for i in removed_ingredients)

        final_price = dish.price - removed_price
        total_price = final_price * quantity

        dish.quantity = quantity
        dish.removed = removed
        dish.final_price = final_price
        dish.total_price = total_price

        total += total_price

        items.append({
            'dish': dish,
            'key': key
        })

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })


def increase_quantity(request, key):
    cart = request.session.get('cart', {})

    if key in cart:
        cart[key]['quantity'] += 1

    request.session['cart'] = cart
    return redirect('cart')


def decrease_quantity(request, key):
    cart = request.session.get('cart', {})

    if key in cart:
        cart[key]['quantity'] -= 1

        if cart[key]['quantity'] <= 0:
            del cart[key]

    request.session['cart'] = cart
    return redirect('cart')


def remove_from_cart(request, key):
    cart = request.session.get('cart', {})

    if key in cart:
        del cart[key]

    request.session['cart'] = cart
    return redirect('cart')


def toggle_like(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)

    liked = False

    if request.user.is_authenticated:

        if request.user in dish.likes.all():
            dish.likes.remove(request.user)

        else:
            dish.likes.add(request.user)
            liked = True

    return JsonResponse({
        'likes': dish.likes.count(),
        'liked': liked
    })


def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    ingredients = dish.ingredients.all()

    return render(request, 'dish_detail.html', {
        'dish': dish,
        'ingredients': ingredients
    })

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    order = Order.objects.create(user=request.user, total_price=0)
    total = 0

    for key, item in cart.items():
        dish_id = key.split("_")[0]
        dish = Dish.objects.get(id=dish_id)

        removed = item['removed']
        quantity = item['quantity']

        removed_ingredients = dish.ingredients.filter(name__in=removed)
        removed_price = sum(i.price for i in removed_ingredients)

        final_price = dish.price - removed_price
        total_price = final_price * quantity

        OrderItem.objects.create(
            order=order,
            dish=dish,
            quantity=quantity
        )

        total += total_price

    order.total_price = total
    order.save()

    request.session['cart'] = {}

    return redirect('profile')

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == 'new':
        order.status = 'canceled'
        order.save()

    return redirect('profile')

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'auth_system/profile.html', {
        'orders': orders
    })