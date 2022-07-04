
from django.contrib import admin
from django.urls import path, include

from authentication.BusinessLogic.NeglectDefaultAuthentications import neglect_authentication
from authentication.Views import SignIn
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', neglect_authentication(SignIn.SignInPage), name='SignInPage'),
    path('signout', neglect_authentication(SignIn.SignInPage), name='SignInPage'),
    path('', include('authentication.urls')),
    path('library/', include('library_app.urls')),
]
urlpatterns += staticfiles_urlpatterns()
