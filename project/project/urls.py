from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('otp/', views.otpverify),
    path('mydata/',views.choose),
    path('showw/',views.show),
    path('uploadd/',views.upload),
    path('thankyou/',views.afterupload),
    path('uploadafile/',views.upload),
    path('gerneratereports/',views.show),
    path('thankyouuu/',views.afterupload),
        
]
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
