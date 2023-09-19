from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.home, name="homepage"),
	path('tienda-de-vinos/', views.store, name="store"),
    path('cata-de-vinos/', views.first_events, name="first_events"),
    path('cata-de-vinos/<slug:slug>', views.event_detail, name="first_event_detail"),
    path('catas-de-vinos/', views.events, name="events"),
    path('<slug:slug>/', views.event_detail, name='event_detail'),   #devo capire come mettere l'evento giusto
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('<slug:slug>/', views.product_detail, name="product_detail"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

]