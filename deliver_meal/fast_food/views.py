from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib.auth import *
from fast_food.forms import *
from fast_food.models import *


# Create your views here.
  # Require authentication for logged-in users
def base_foods(request):
    foods = Food.objects.all()
    
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, shipped=False)
    else:
        orders = None

        
    
    return render(request, 'base.html', {'foods': foods, 'orders': orders})



@login_required
def add_to_basket(request, food_id):
    # Check if the user is logged in
    if not request.user.is_authenticated:
        # Redirect to the login page
        return redirect('base')

    # Filter orders by user and not shipped
    order, created = Order.objects.get_or_create(user=request.user, shipped=False)

    # Get the food item
    food = get_object_or_404(Food, pk=food_id)

    # Check if the order item already exists
    order_item, created = OrderItem.objects.get_or_create(order=order, food=food)

    # If the item already exists, increment the quantity
    if not created:
        order_item.quantity += 1
    else:
        # If the item is created for the first time, set an initial quantity
        order_item.quantity = 1

    # Save the order item
    order_item.save()

    # Redirect to the home page after adding the item to the basket
    return redirect('base_foods')

    # The code below will not be executed after the redirect

    orders = Order.objects.filter(user=request.user, shipped=False)
    orders1 = Order.objects.filter(user=request.user, shipped=False)

    return render(request, 'added_to_basket.html', {'food': food, 'order': order, 'orders1': orders1, 'orders': orders})
def navbar(request):
    orders = Order.objects.filter(user=request.user, shipped=False)
    return render(request, 'navbar.html',{'orders':orders})


def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    order1 = order.overall_price()
    return render(request, 'order_detail.html', {'order': order,'order1':order1})
@require_POST
def change_quantity(request, item_id1, change1):
    order_item = get_object_or_404(OrderItem, pk=item_id1)

    # Validate that the user making the request is the owner of the order
    if request.user != order_item.order.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    new_quantity1 = order_item.quantity + change1

    # Ensure the quantity is non-negative
    if new_quantity1 >= 0:
        order_item.quantity = new_quantity1
        order_item.save()

        # Update total price in the order
        order_item.order.total_price = order_item.order.orderitem_set.aggregate(Sum('quantity'))['quantity__sum']
        order_item.order.save()

        # Redirect to the home page
        order_detail_url = reverse('order_detail', args=[order_item.order.id])
        return redirect(order_detail_url) # Replace 'home' with the actual name or URL of your home page

    return JsonResponse({'error': 'Invalid quantity'}, status=400)



@require_POST
def decrase_quantity(request, item_id, change):
    order_item = get_object_or_404(OrderItem, pk=item_id)

    # Validate that the user making the request is the owner of the order
    if request.user != order_item.order.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    new_quantity = order_item.quantity - change

    # Ensure the quantity is non-negative
    if new_quantity >= 0:
        order_item.quantity = new_quantity
        order_item.save()

        # Update total price in the order
        order_item.order.total_price = order_item.order.orderitem_set.aggregate(Sum('quantity'))['quantity__sum']
        order_item.order.save()

        if new_quantity == 0:
            order_item.delete()
            order_detail_url = reverse('order_detail', args=[order_item.order.id])
            return redirect(order_detail_url)
            #return JsonResponse({'success': True, 'deleted': True})
        order_detail_url = reverse('order_detail', args=[order_item.order.id])
        return redirect(order_detail_url)
        #return JsonResponse(
           # {'success': True, 'new_quantity': new_quantity, 'new_total_price': order_item.order.total_price})

    return JsonResponse({'error': 'Invalid quantity'}, status=400)

@require_POST
def delete_item(request, item_id):
    order_item = get_object_or_404(OrderItem, pk=item_id)

    # Validate that the user making the request is the owner of the order
    if request.user != order_item.order.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    # Get the order associated with the item
    order = order_item.order

    # Delete the item
    order_item.delete()

    # Update total price in the order
    order.total_price = order.orderitem_set.aggregate(Sum('quantity'))['quantity__sum']
    order.save()
    order_detail_url = reverse('order_detail', args=[order_item.order.id])
    return redirect(order_detail_url)

    #return JsonResponse({'success': True, 'new_total_price': order.total_price})


@login_required
def create_shipment(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            shipment = form.save(commit=False)
            shipment.order = order  # Set the order before saving
            shipment.save()

            # Update the order's shipped status
            order.shipped = True
            order.save()

            return redirect('shipment_detail', order_id=order.id)
    else:
        form = ShipmentForm()

    return render(request, 'create_order.html', {'form': form, 'order': order})



@login_required
def shipment_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    shipment = get_object_or_404(Shipment, order_id=order_id, order__user=request.user)
    overall_price = sum(item.get_total() for item in order.orderitem_set.all())
    order1 = order.product_all_quantity()

    username = request.user.username
    return render(request, 'shipment_detail.html', {'shipment': shipment,'order':order,'username': username,'overall_price': overall_price,'order1':order1})
#authications

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('base_foods')  # Redirect to your home page or any other page after signup
    else:
        form = SignUpForm()
    return render(request, 'sighnup.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('base_foods')

def user_login(request):
    if request.method == 'POST':
        form =  LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('base_foods')  # Redirect to your home page or any other page after login
    else:
        form =  LoginForm()
    return render(request, 'login.html', {'form': form})


# for features for admin staff


@staff_member_required()
def admin_order_list(request):
    orders1 = Order.objects.filter(shipped=True)




    return render(request, 'admin_order_list.html', {'orders1': orders1,})



@staff_member_required
def admin_shipment_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    shipment = get_object_or_404(Shipment, order=order)

    username = order.user.username

    # Calculate overall price
    overall_price = sum(item.get_total() for item in order.orderitem_set.all())
    order1 = order.product_all_quantity()
    order_overall_price = order.overall_price()

    return render(request, 'admin_shipment_detail.html', {'shipment': shipment,'order1':order1,' order_overall_price': order_overall_price, 'username': username,'order': order, 'overall_price': overall_price})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'admin_order_detail.html', {'order': order})


def admin_main_page(request):
    return render(request , 'admin_navbar.html')
