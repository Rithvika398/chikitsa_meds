from django.shortcuts import render
from .models import Medicines,Appt,Doctor,Product, Variation, VARIATION_CATEGORIES, Cart, CartItem,Order
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserForm, ApptForm
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import datetime,date
from django.urls import reverse
from django.contrib import messages
import random
import string
import datetime
from django.shortcuts import render, redirect
from django.template import RequestContext
from decimal import Decimal
from django.shortcuts import render, HttpResponseRedirect
from .utils import OrderIdGenerator





unicode = str


# Create your views here.
def homepage(request):
    #all_albums= Album.objects.all()
    template= loader.get_template('homepage/home.html')
    context = {}
    '''
    context= {
        'all_albums': all_albums
    }
      
    html=''
    for album in all_albums:
        url = '/testapp/'+ str(album.id)
        html += '<a href="'+ url + '">'+ album.album_title+ '</a><br>'
    '''
    return render(request, 'homepage/home.html', context)
    #return HttpResponse(template.render(request))

def medicines(request):
    meds=Medicines.objects.all()
    template= loader.get_template('homepage/meds.html')
    context = {
        'meds': meds
    }
    return render(request, 'homepage/meds.html', context)
def contact(request):
    context={}
    return render(request, 'homepage/contact.html', context)
def bookappt(request):
    context={}
    return render(request, "<h1>Coming soon!</h1>", context)

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'homepage/login.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #albums = Medicines.objects.filter(user=request.user)
                return render(request, 'homepage/home.html', {})
            else:
                return render(request, 'homepage/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'homepage/login.html', {'error_message': 'Invalid login'})
    return render(request, 'homepage/login.html')


def bookappt(request):
    if not request.user.is_authenticated:
        return render(request, 'homepage/login.html')
    else:
        form = ApptForm(request.POST or None)
        age=0
        time='2018-08-18 14:06:44.176830+00:00'
        doctor="Sinha"

        if form.is_valid():
            appt = form.save(commit=False)
            appt.user = request.user
            appt.save()
            age=form.cleaned_data['age']
            time=timezone.now()
            #time=form.cleaned_data['time']
            doctor=form.cleaned_data['doctor']
            form=ApptForm()
            appt.save()


            #return render(request, 'homepage/detail.html', {'appt': appt})
        context = {
            "form": form,
            "age":age,
            "time":time,
            "doctor":doctor,

        }
        return render(request, 'homepage/bookappt.html', context)



def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.is_superuser = True
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)

    context = {
        "form": form,
    }
    return render(request, 'homepage/signup.html', context)

def detail(request, appt_id):
    if not request.user.is_authenticated():
        return render(request, 'homepage/login.html')
    else:
        user = request.user
        appts = get_object_or_404(Appt, pk=appt_id)
        return render(request, 'homepage/detail.html', {'appt': appts, 'user': user})
'''
def my_profile(request):
    my_user_profile=Profile.objects.filter(user=request.user).first()
    my_orders=Order.objects.filter(is_ordered=True,owner=my_user_profile)
    context={
        'my_orders': my_orders
    }
    return render(request, "profile.html", context)

def product_list(request):
    object_list=Medicines.objects.all()
    filtered_orders= Order.objects.filter(owner=request.user.profile, is_order=True)
    current_order_products=[]
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items= user_order.items.all()
        current_order_products=[product.product for product in user_order_items]
        context={
            'object_list':object_list,
            'current_order_products': current_order_products
        }
        return render(request,"homepage/product_list.html", context)
@login_required()
def add_to_cart(request, **kwargs):
    user_profile=get_object_or_404(Profile, user=request.user)
    product=Medicines.objects.filter(id=kwargs.get('item_id', "")).first()
    if product in request.user.profile.meds.all():
        messages.info(request, 'You already own this medicine')
        return redirect(reverse('product-list'))
    order_item, status=Order.objects.get_or_create(product=product)
    user_order, status=Order.objects.get_or_create(owner=user_profile,is_ordered=True)
    user_order.items.add(order_item)
    if status:
        user_order.ref_code=generate_order_id()
        user_order.save()

    messages.info(request,"Item added to cart")
    return redirect(reverse('product-list'))

@login_required()
def delete_from_cart(request, item_id):
    item_to_delete=OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
        return redirect(reverse('order_summary'))

@login_required()
def order_details(request, **kwargs):
    existing_order=get_user_pending_order(request)
    context={
        'order':existing_order
    }
    return render(request, 'order_summary.html', context)


def checkout(request):
    existing_order=get_user_pending_order(request)
    context={
        'order': existing_order
    }
    return render(request, 'checkout.html', context)

@login_required()
def update_transaction_records(request, order_id):
    order_to_purchase=Order.objects.filter(pk=order_id).first()
    order_to_purchase.is_ordered=True
    order_to_purchase.date_ordered=datetime.datetime.now()
    order_to_purchase.save()

    order_items=order_to_purchase.items.all()
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())


    user_profile=get_object_or_404(Profile, user = request.user)

    order_products=[item.product for item in order_items]
    user_profile.meds.add(*order_products)
    user_profile.save()

    messages.info(request, "Thank You! Your items have been added!")
    return redirect(reverse('my_profile'))
def success(request, **kwargs):
    return render(request, 'purchase_success.html', {})

def get_user_pending_order(request):
    user_profile= get_object_or_404(Profile, user=request.user)
    order= Order.objects.filter(owner=user_profile,is_ordered=False)
    if order.exists():
        return order[0]
    return 0
def saveOrderItem(order):
    order_item=OrderItem.objects.get_or_create(order=order)
    order_item.save()
    return order_item
def generate_order_id():
    date_str=date.today().strftime('%Y%m%d')[2:]+ str(datetime.datetime.now)
    rand_str="".join([random.choice(string.digits) for count in range(3)])
    return date_str +rand_str
'''
def get_user_cart(request):
    """Retrieves the shopping cart for the current user."""
    cart_id = None
    cart = None
    # If the user is logged in, then grab the user's cart info.
    if request.user.is_authenticated and not request.user.is_anonymous:
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart(user=request.user)
            cart.save()
    else:
        cart_id = request.session.get('cart_id')
        if not cart_id:
            cart = Cart()
            cart.save()
            request.session['cart_id'] = cart.id
        else:
            cart = Cart.objects.get(id=cart_id)
    return cart


def get_cart_count(request):
    cart = get_user_cart(request)
    total_count = 0
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        total_count += item.quantity
    return total_count


def update_cart_info(request):
    request.session['cart_count'] = get_cart_count(request)


def view_cart(request):
    cart = get_user_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    order_total = Decimal(0.0)
    for item in cart_items:
        order_total += (item.product.price * item.quantity)

    context={
        'cart':cart,
        'cart_items':cart_items,
        'order_total':order_total

    }
    return render(request,'homepage/view_cart.html',context )


def add_to_cart(request, slug):
    if request.POST:
        cart = get_user_cart(request)
        product = Product.objects.get(slug=slug)
        quantity = int(request.POST.get('qty')) or 1
        variations = []
        for variation_group in VARIATION_CATEGORIES:
            variation_id = request.POST.get(variation_group[0], None)
            print( 'Variation' + unicode(variation_id))
            if variation_id:
                variations.append(variation_id)
        cart_item = CartItem(product=product, cart=cart, quantity=0)
        cart_item.quantity += quantity
        cart_item.save()
        for variation_id in variations:
            cart_item.variations.add(Variation.objects.get(id=int(variation_id)))
        if request.session.get('cart_count'):
            request.session['cart_count'] += quantity
        else:
            request.session['cart_count'] = quantity
        update_cart_info(request)
    return redirect(reverse('view_cart'))


def remove_from_cart(request, id):
    if request.POST:
        cart_item = CartItem.objects.get(id=id)
        quantity = cart_item.quantity
        cart_item.delete()
        if request.session.get('cart_count'):
            request.session['cart_count'] -= quantity
        else:
            request.session['cart_count'] = 0
        update_cart_info(request)
        return redirect(reverse('view_cart'))

@login_required
def checkout(request):
    try:
        cart_id = request.session['cart_id']
    except KeyError:
        #return HttpResponseRedirect(reverse('view_cart'))
        return render(request,'homepage/checkout.html', {})

    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        #return HttpResponseRedirect(reverse('view_cart'))
        return render(request,'homepage/checkout.html', {})


    try:
        order = Order.objects.get(cart=cart)
    except Order.DoesNotExist:
        order_id = OrderIdGenerator.generate_order_id()
        # TODO: Allow anonymous users to checkout
        order = Order(cart=cart, id=order_id, user=request.user)
        order.save()

    if order.status == 'finished':
        try:
            del request.session['cart_id']
            del request.session['cart_count']
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('view_cart'))
    context = {
        'order': order
    }
    template = 'homepage/checkout.html'
    return render(request, template, context)

@login_required
def orders(request):
    order=Order.objects.filter(user=request.user)
    context = {'order':order}
    template = 'homepage/orders.html'
    return render(request, template, context)

def all(request):
    all_products = Product.objects.all()
    print(all_products)
    return render(request, 'homepage/all.html', {'all_products': all_products})


def detail(request, slug):
    print (slug)
    # try:
    product = Product.objects.get(slug=slug)
    # except:
    # raise Http404
    return render(request, 'homepage/detail.html',{'product': product})


def search(request):
    search_query = request.GET.get('name')
    results = Product.objects.filter(title__icontains=search_query)
    context={
        'search_query':search_query,
        'results':results
    }
    return render(request,'homepage/search.html',context )


















