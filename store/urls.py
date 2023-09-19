from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.home, name="homepage"),
	path('tienda-de-vinos/', views.store, name="store"),
    path('tienda-de-vinos/<slug:slug>/', views.product_detail, name="product_detail"),
    path('cata-de-vinos/', views.first_events, name="first_events"),
    path('cata-de-vinos/', views.events, name="events"),
    path('cata-de-vinos/<slug:slug>/', views.event_detail, name='event_detail'),   #devo capire come mettere l'evento giusto
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

]