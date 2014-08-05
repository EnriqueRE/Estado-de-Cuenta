from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from Estado import views

from django.contrib import admin

admin.autodiscover()

router = DefaultRouter()
router.register(r'User', views.UserViewSet)
router.register(r'Statement', views.StatementViewSet)

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'EstadoDeCuenta.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^ldap/',
                           'Estado.views.checkUserInLdap'),
                       url(r'^Statement_Search',
                           views.StatementSearch.as_view(
                               model='AccountStatement')),
                       url(r'^', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls',
                                                  namespace='rest_framework')),
)
