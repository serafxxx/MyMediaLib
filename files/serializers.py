import logging
from django.conf import settings
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from files.models import MyFile, PhotoFile, VideoFile, Imprt, RawPhoto


log = logging.getLogger(__name__)

class MySerializer(ModelSerializer):
    cls = SerializerMethodField()

    def get_cls(self, obj):
        return obj.__class__.__name__

class MyFileSerializer(MySerializer):
    src = SerializerMethodField()
    thumb = SerializerMethodField()

    class Meta:
        model = MyFile
        exclude = ('hash', '_thumb', '_preview')

    def get_src(self, obj):
        return obj.path.replace(settings.MEDIA_ROOT + '/', settings.MEDIA_URL)

    def get_thumb(self, obj):
        try:
            return obj.thumb.replace(settings.MEDIA_ROOT + '/', settings.MEDIA_URL)
        except NotImplementedError:
            return ''
        except Exception as e:
            log.exception(e)
            return ''

class PhotoFileSerializerShort(MyFileSerializer):
    class Meta(MyFileSerializer.Meta):
        model = PhotoFile
        fields = ('id', 'cls', 'thumb', 'created_date')
        exclude = None


class PhotoFileSerializer(MyFileSerializer):
    preview = SerializerMethodField()
    class Meta(MyFileSerializer.Meta):
        model = PhotoFile

    def get_preview(self, obj):
        try:
            return obj.preview.replace(settings.MEDIA_ROOT + '/', settings.MEDIA_URL)
        except NotImplementedError:
            return ''
        except Exception as e:
            log.exception(e)
            return ''


class VideoFileSerializer(MyFileSerializer):
    class Meta(MyFileSerializer.Meta):
        model = VideoFile


class RawPhotoSerializerShort(MyFileSerializer):
    class Meta(MyFileSerializer.Meta):
        model = RawPhoto
        fields = ('id', 'cls', 'thumb', 'created_date')
        exclude = None


class RawPhotoSerializer(MyFileSerializer):
    preview = SerializerMethodField()
    class Meta(MyFileSerializer.Meta):
        model = RawPhoto

    def get_preview(self, obj):
        try:
            return obj.preview.replace(settings.MEDIA_ROOT + '/', settings.MEDIA_URL)
        except NotImplementedError:
            return ''
        except Exception as e:
            log.exception(e)
            return ''


class ImprtSerializer(ModelSerializer):
    class Meta:
        model = Imprt
