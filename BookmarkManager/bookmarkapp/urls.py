from django.urls import path
from django.conf.urls import url
from bookmarkapp import views

urlpatterns = [
	# Api for create
    url('create',views.create,name='create'),
    # Api for browse
    url(r'^browse/$',views.browse,name='getSymbolData'),
]