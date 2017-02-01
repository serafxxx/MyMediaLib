import pytz
from itertools import chain
from operator import attrgetter

from rest_framework import viewsets, generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.serializers import ModelSerializer

import MyMediaLib.settings as settings

from files.models import PhotoFile, MyFile, VideoFile, Imprt, RawPhoto
from datetime import datetime, timedelta

from files.serializers import MyFileSerializer, PhotoFileSerializer, PhotoFileSerializerShort, VideoFileSerializer, ImprtSerializer, RawPhotoSerializerShort, RawPhotoSerializer
from util.decorators import cache_result


def serialize_media(media, short=False):
    '''Serialize any structure with media files'''

    serializers = {
        'PhotoFile': PhotoFileSerializer,
        'VideoFile': VideoFileSerializer,
        'RawPhoto': RawPhotoSerializer
    }
    if short:
        serializers = {
            'PhotoFile': PhotoFileSerializerShort,
            'VideoFile': VideoFileSerializer,
            'RawPhoto': RawPhotoSerializerShort
        }

    if type(media) == dict:
        new_media = {}
        for k in media:
            new_media[k] = serialize_media(media[k], short)
        return new_media
    elif type(media) == list:
        new_media = []
        for i in range(len(media)):
            new_media.append(serialize_media(media[i], short))
        return new_media
    else:
        if media.__class__.__name__ in serializers:
            serializer = serializers[media.__class__.__name__]
            return serializer(media).data

        return media


# @cache_result()
# def media_sort_by_type(date_low, date_high):
#     media = {}
#     media['PhotoFile'] = [f for f in PhotoFile.objects.filter(created_date__gte=date_low, created_date__lt=date_high)]
#     media['VideoFile'] = [f for f in VideoFile.objects.filter(created_date__gte=date_low, created_date__lt=date_high)]
#     return media
#
# @cache_result()
# def media_sort_by_date_raw(date_low, date_high):
#     media_by_date_raw = []
#     media_by_type = media_sort_by_type(date_low, date_high)
#     for cls in media_by_type:
#         media_by_date_raw.extend(media_by_type[cls])
#     media_by_date_raw.sort(key=lambda f: f.created_date)
#     return media_by_date_raw

# def media_sort_by_date(date_low, date_high):
#     media_by_date = {}
#     media_by_date_raw = media_sort_by_date_raw(date_low, date_high)
#     for f in media_by_date_raw:
#         cd = f.created_date
#         if cd.year not in media_by_date:
#             media_by_date[cd.year] = {}
#         if cd.month not in media_by_date[cd.year]:
#             media_by_date[cd.year][cd.month] = {}
#         if cd.day not in media_by_date[cd.year][cd.month]:
#             media_by_date[cd.year][cd.month][cd.day] = []
#
#         media_by_date[cd.year][cd.month][cd.day].append(f)
#     return media_by_date


def get_media(date_low, date_high):
    photo_files = PhotoFile.objects.filter(created_date__gte=date_low, created_date__lt=date_high)
    video_files = VideoFile.objects.filter(created_date__gte=date_low, created_date__lt=date_high)
    raw_photo_files = RawPhoto.objects.filter(created_date__gte=date_low, created_date__lt=date_high)

    return sorted( chain(photo_files, video_files, raw_photo_files), key=attrgetter('created_date'))

@api_view(['GET'])
def years_list(request):
    '''List available years'''
    dates = MyFile.objects.dates('created_date', 'year')
    years = [d.year for d in dates]
    return Response({'years':years})


@api_view(['GET'])
def year_detail(request, year):
    year = int(year)
    date_low = datetime(year=year, month=1, day=1, tzinfo=pytz.timezone(settings.TIME_ZONE))
    date_high = datetime(year=year+1, month=1, day=1, tzinfo=pytz.timezone(settings.TIME_ZONE))
    # media = get_media(date_low, date_high)
    months = [d.month for d in MyFile.objects.filter(created_date__gte=date_low, created_date__lt=date_high).dates('created_date', 'month')]

    resp = {}
    for month in months:
        next_month = 1 if month == 12 else month + 1
        next_year = year + 1 if next_month == 1 else year
        month_start = datetime(year, month, 1)
        month_end = datetime(next_year, next_month, 1)
        resp[month] = get_media(month_start, month_end)[:20]

    return Response({
        'months':serialize_media(resp, short=True)
    })


@api_view(['GET'])
def month_detail(request, year, month):
    year = int(year)
    month = int(month)
    next_month = 1 if month == 12 else month+1
    next_year = year+1 if next_month == 1 else year

    date_low = datetime(year=year, month=month, day=1, tzinfo=pytz.timezone(settings.TIME_ZONE))
    date_high = datetime(year=next_year, month=next_month, day=1, tzinfo=pytz.timezone(settings.TIME_ZONE))

    # media = get_media(date_low, date_high, request.GET.get('sort'))
    media = get_media(date_low, date_high)

    return Response({
        'date_low': date_low,
        'date_high': date_high,
        'media': serialize_media(media, short=True)
    })

@api_view(['GET'])
def day_detail(request, year, month, day):
    year = int(year)
    month = int(month)
    day = int(day)
    date_low = datetime(year=year, month=month, day=day, tzinfo=pytz.timezone(settings.TIME_ZONE))
    date_high = date_low + timedelta(days=1)

    media = get_media(date_low, date_high, request.GET.get('sort'))

    return Response(serialize_media(media, short=True))

############################################ COMMON VIEWS Probably remove later

# class MyFileViewSet(viewsets.ModelViewSet):
#     serializer_class = MyFileSerializer
#
#     def get_queryset(self):
#         return MyFile.objects.all()


class PhotoFileViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = PhotoFileSerializer
    queryset = PhotoFile.objects.all()

class RawPhotoViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = RawPhotoSerializer
    queryset = RawPhoto.objects.all()


# class VideoFileViewSet(viewsets.ModelViewSet):
#     serializer_class = VideoFileSerializer
#
#     def get_queryset(self):
#         return VideoFile.objects.all()
#
#
# class ImprtViewSet(viewsets.ModelViewSet):
#     serializer_class = ImprtSerializer
#
#     def get_queryset(self):
#         return Imprt.objects.all()
