from django.urls import path

from . import views
from .views import ProductLandingPageView, SuccessView, CancelView, StripeIntentView


urlpatterns = [
	#Leave as empty string for base url
	path('', views.home, name="homepage"),
	path('tienda-de-vinos/', views.store, name="store"),
    path('tienda-de-vinos/<slug:slug>/',views.product_detail, name="product_detail"),
    path('cata-de-vinos/', views.first_events, name="first_events"),
    path('catas-de-vinos/', views.events, name="events"),
    path('cata-de-vinos/<slug:slug>/', views.event_detail, name='event_detail'),   #devo capire come mettere l'evento giusto
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('contactenos/', views.contacts, name="contacts"),
    #path('checkout/', views.ProductLandingPageView.as_view(), name="checkout"),
    path('search/', views.search_results, name="search_results"),
    path('tienda-de-vinos/<str:tipo>', views.filters, name="filtered_results"),



    #stripe conf urls


    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('landing/', ProductLandingPageView.as_view(), name='landing-page'),
    #path('landing/', views.ProductLandingPageView.as_view(), name='landing-page'),
    path('create-payment-intent/<pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('create-checkout-session/<pk>/', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('webhooks/stripe/', views.stripe_webhook, name='stripe-webhook'),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

]