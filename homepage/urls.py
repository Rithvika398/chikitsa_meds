from django.contrib import admin
from django.conf.urls import url,include
from django.conf.urls import url
from django.urls import is_valid_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^homepage/$', views.homepage, name='homepage'),
    url(r'^medicines/$', views.all, name='medicines'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^bookappt/$', views.bookappt, name='bookappt'),
    url(r'^signup/$', views.register, name='signup'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

                  #url(r'^add-to-cart/(?P<item_id>[-\w]+)/$', views.add_to_cart, name='add_to_cart'),
    #url(r'^order-summary/$', views.order_details, name='order_summary'),
    #url(r'^login/$', views.login_user, name='login'),
    url(r'^products/(?P<slug>[^\/]+)\/add$', views.add_to_cart, name='add_to_cart'),
    url(r'^products/(?P<id>\d+)\/remove$', views.remove_from_cart,name='remove_from_cart'),
    url(r'^products/(?P<slug>[^\/]+)\/?', views.detail, name='detail'),
    url(r'^products/$', views.all, name='all'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search/(?P<search_id>.+)/', views.search, name='results'),

    url(r'^cart/$', views.view_cart, name='view_cart'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^orders/$', views.orders, name='orders'),

                  #url(r'^index/$', views.index, name='index'),

              ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
