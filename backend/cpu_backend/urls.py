from django.contrib import admin
from django.views.generic.edit import CreateView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, reverse_lazy

from users.forms import CustomUserCreationForm

urlpatterns = [
    path('', include('cpus.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=CustomUserCreationForm,
            success_url=reverse_lazy('cpus:index'),
        ),
        name='registration',
    ),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Если проект запущен в режиме разработки
if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

handler404 = 'core.views.page_not_found'
