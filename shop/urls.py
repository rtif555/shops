from django.conf.urls import patterns, include, url
from shop.furnitures.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'shop.views.home', name='home'),
    # url(r'^shop/', include('shop.foo.urls')),
    (r'^$', home),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'C:/Python25/shop/shop/media'}),
    # Uncomment the next line to enable the admin:
    (r'^admin/statistic/$', statistics),
    url(r'^admin/', include(admin.site.urls)),
    (r'^avtoriz/$', avtorization),
    (r'^avtoriz/enter[/]{0,1}$', enter),
    (r'^logout/$', logout),

    (r'^basket(\d+)/$',basket),
    (r'^basket(\d+)/all[/]{0,1}$',buyall),
    (r'^cancel/buy/(\d+)/(\d+)/',cancel_product),
    (r'^cancel/orders/(\d+)[/]{0,1}$',cancel_orders),

    (r'^help/$', help),
	
    (r'^find/(\d*)[/]{0,1}$', find),
    (r'^furniture/(\d+)/(\d*)[/]{0,1}$', buy_web),
    (r'^furniture/(\d+)/(\d*)[/]{0,1}buy/$', buy),
    
    (r'^indification/(\d+)/$', internetorder),
    (r'^internetorders/$', buyinternetorder),

  
	
    (r'^storekeeper/$', store),
	(r'^storekeeper/see/$', store_see_furniture),
    (r'^storekeeper/order/(\d+)[/]{0,1}$', storeorder),
    (r'^storekeeper/order/(\d+)/give[/]{0,1}$',storeordergive),
    (r'^storekeeper/get$',storeget),
    (r'^furniture/update/(\d+)[/]{0,1}$',storeupdate),
)
