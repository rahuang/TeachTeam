from django.conf.urls import patterns, include, url
from django.contrib import admin

from ClassConnect import views

# Override the Admin Site header
admin.site.site_header = "Django Template Administration"

# Set the error handlers
handler403 = views.PermissionDeniedView.as_view()
handler404 = views.NotFoundView.as_view()
handler500 = views.ErrorView.as_view()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ClassConnect.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^classes$', views.ClassesPage.as_view(), name='classes'),
    url(r'^class/$', views.ClassPage.as_view(), name='class'),
    url(r'^messaging$', views.MessagingPage.as_view(), name='msg'),
    url(r'^email$', views.EmailPage.as_view(), name='email'),
    url(r'^process-email$', views.ProcessEmailPage.as_view(), name='processemail'),
    url(r'^gradebook$', views.GradeBookPage.as_view(), name='gradebook'),
    url(r'^$', views.LoginPage.as_view(), name='login'),
    
    url(r'^test/', include('testapp.urls')),
    url(r'^users/', include('users.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
)
