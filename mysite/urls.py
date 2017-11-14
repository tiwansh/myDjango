from django.conf.urls import include, url
from django.contrib import admin
import blog.urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'', include('blog.urls')),
]
