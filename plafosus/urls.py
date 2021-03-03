from django.contrib import admin
from django.urls import path, re_path, reverse_lazy
from django.views.generic import RedirectView


admin.site.site_header = 'PLAFOSUS'
admin.site.site_title = 'PLAFOSUS'
admin.site.index_title = 'PLAFOSUS administration'

urlpatterns = [
    # The Django admin page.
    path('admin/', admin.site.urls),

    # Redirects to the django admin login, when going to base address.
    re_path(r'^$', RedirectView.as_view(url='/admin')),

]
