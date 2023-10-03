from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
import stripe
from django.conf import settings
from ecommerce.config import EMAIL_HOST_USER
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.db.models import Q, Count
from django.core.mail import send_mail
from random import sample









def home(request):
	return render(request,'store/homepage.html',{})

def events(request):
		data = cartData(request)
		cartItems = data['cartItems']
		order = data['order']
		items = data['items']
		oggi=datetime.date.today()
		# Filtra i prodotti della categoria "Degustazioni di vini"
		products = Cata.objects.all().filter(date__gte=oggi).order_by('date')

		context = {'products': products, 'cartItems': cartItems}
		return render(request, 'store/events_catas.html', context)



def first_events(request):
		data = cartData(request)
		cartItems = data['cartItems']
		order = data['order']
		items = data['items']
		oggi=datetime.date.today()
		
		
		products = Cata.objects.filter(date__gte=oggi).order_by('date')[:2]
		context = {'products': products, 'cartItems': cartItems}
		return render(request, 'store/provacatas.html', context)

def event_detail(request, slug):
	data=cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	product = get_object_or_404(Cata, slug=slug)
	context = {'product': product, 'cartItems': cartItems}
	return render(request, 'store/event_detail.html', context)





def store(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	products = Vino.objects.all()

	all_bodegas = Vino.objects.values_list('bodega', flat=True).distinct()
	bodegas_list=list(all_bodegas)

	all_tipos = Vino.objects.exclude(tipo='').values_list('tipo', flat=True).distinct()
	tipos_list = list(all_tipos)


	context = {'products': products, 'cartItems': cartItems, 'bodegas_list':bodegas_list, 'tipos_list':tipos_list}
	return render(request, 'store/store.html', context)


def search_results(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	query = request.GET.get("q")
	products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
	return render(request, 'store/search_results.html', {'products': products, 'cartItems':cartItems})


def filters(request,tipo):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Vino.objects.filter(Q(tipo__icontains=tipo))


	context = {'products': products, 'cartItems': cartItems}
	return render(request, 'store/product_filtered.html', context)



def product_detail(request, slug):
	data = cartData(request)
	cartItems = data['cartItems']	
	order = data['order']
	items = data['items']

    # Filtra i prodotti della categoria "Vini"
    
	product = get_object_or_404(Vino, slug=slug)
	related_products_queryset = Vino.objects.filter(Q(bodega=product.bodega) | Q(denomination=product.denomination)).exclude(slug=slug)
	related_products = sample(list(related_products_queryset), min(4, related_products_queryset.count()))

	context = {'product': product, 'cartItems': cartItems, 'related_products':related_products}
	return render(request, 'store/product_detail_originale.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)








def contacts(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			user_email = form.cleaned_data['email']
			subject = 'Confirmation: Your Message Has Been Received'
			message = 'Thank you for your message. We have received it successfully.'
			from_email = EMAIL_HOST_USER # Your email address
			recipient_list = [user_email,]
			send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            # After sending the email, redirect to the confirmation page
		return render(request, 'store/confirmation.html')
	else:
		form = ContactForm()

	return render(request, 'store/contacts.html', {'form': form})
##STRIPE
stripe.api_key = settings.STRIPE_SECRET_KEY

class ProductLandingPageView(TemplateView):
    template_name = "store/landing.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="test")
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context



#Checkout session endpoint



class SuccessView(TemplateView):
    template_name = "store/success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"



"""
class product_detail(View):
    template_name = "product_detail.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Test Product")
        context = super(product_detail, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context"""



class CreateCheckoutSessionView(View):
	def post(self, request, *args, **kwargs):
		product_id = self.kwargs["pk"]
		product = Product.objects.get(id=product_id)
		print(product)
		YOUR_DOMAIN = "http://127.0.0.1:8000"
		checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
			metadata={
                "product_id": product.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
		return JsonResponse({
            'id': checkout_session.id
        })



@csrf_exempt
def stripe_webhook(request):
	payload = request.body
	sig_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None

	try:
		event = stripe.Webhook.construct_event(
			payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
		)
	except ValueError as e:
		# Invalid payload
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		# Invalid signature
		return HttpResponse(status=400)
	  # Handle the checkout.session.completed event
	if event['type'] == 'checkout.session.completed':
		# Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
		session = stripe.checkout.Session.retrieve(
		event['data']['object']['id'],
		expand=['line_items'],
		)
		line_items = session.line_items
		# Fulfill the purchase...
		#fulfill_order(line_items)
		print(session)
		customer_email = session["customer_details"]["email"]
		product_id = session["metadata"]["product_id"]
		product = Product.objects.get(id=product_id)
		send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
            recipient_list=[customer_email],
            from_email="admin@amavinos.com"
        )
	elif event["type"] == "payment_intent.succeeded":
		intent = event['data']['object']

		stripe_customer_id = intent["customer"]
		stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

		customer_email = stripe_customer['email']
		product_id = intent["metadata"]["product_id"]

		product = Product.objects.get(id=product_id)

		send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
            recipient_list=[customer_email],
            from_email="matt@test.com"
        )


	# Passed signature verification
	return HttpResponse(status=200)





class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            product_id = self.kwargs["pk"]
            product = Product.objects.get(id=product_id)
            intent = stripe.PaymentIntent.create(
                amount=product.price,
                currency='eur',
                customer=customer['id'],
                metadata={
                    "product_id": product.id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({ 'error': str(e) })





