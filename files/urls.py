from django.conf.urls import url, include
from files import views


from rest_framework.routers import DefaultRouter

from files.views import PhotoFileViewSet, RawPhotoViewSet

router = DefaultRouter()
# router.register(r'myfiles', MyFileViewSet, 'MyFile')
router.register(r'photo-files', PhotoFileViewSet, 'PhotoFile')
router.register(r'raw-photos', RawPhotoViewSet, 'RawPhoto')
# router.register(r'video-files', VideoFileViewSet, 'VideoFile')
# router.register(r'imprts', ImprtViewSet, 'Imprt')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^dates/$', views.years_list),
    url(r'^dates/(?P<year>[0-9]{4})/?$', views.year_detail),
    url(r'^dates/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/?$', views.month_detail),
    url(r'^dates/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/?$', views.day_detail)
]