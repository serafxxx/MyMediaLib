from __future__ import unicode_literals

import StringIO
import hashlib
import shutil
import subprocess

import os
import re

import logging
import struct
import pytz as pytz
from datetime import datetime

from django.db import models

from PIL import Image
# from wand.image import Image as WandImage

import MyMediaLib.settings as settings
from util import hashfile, maybe_add_number_to_file_name, mkdir_p, crop_rect
from util.my_exceptions import MyException
from util.exiftool import ExifTool

log = logging.getLogger(__name__)

class MyFile(models.Model):

    imported_date = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(null=True, blank=True, default=None, help_text='Date from file metadata')
    hash = models.CharField(max_length=64, db_index=True, unique=True, help_text='Unique file identifier')
    path = models.CharField(max_length=512, help_text='File path')
    imported_from_path = models.CharField(max_length=512, blank=True, help_text='File path as was before import, for history')
    imprt = models.ForeignKey('Imprt', related_name='myfiles', on_delete=models.CASCADE, help_text='All files from one import have same imprt object')
    _thumb = models.CharField(max_length=512, help_text='Thumb path', blank=True, null=True, default=None)
    _preview = models.CharField(max_length=512, help_text='Preview path', blank=True, null=True, default=None)
    is_system = models.BooleanField(default=False, help_text='If file needs to be hidden')

    def start_exiftool(function):
        '''Decorator to use for MyFile methods.
        It ensures that ExifTool instance is running. Use it for all methods where ExifTool is using.
        '''
        def wrapper(self, *args, **kw):

            if not hasattr(self, '_exiftool') or not self._exiftool:
                # Make an instance of ExifTool
                self._exiftool = ExifTool(executable_=settings.EXIFTOOL_PATH)

            if not self._exiftool.running:
                self._exiftool.start()
                ret = function(self, *args, **kw)
                self._exiftool.terminate()
            else:
                ret = function(self, *args, **kw)
            return ret
        return wrapper

    def set_exiftool(self, exiftool):
        self._exiftool = exiftool

    def __str__(self):
        return self.path.replace(settings.MEDIA_LIB, '')

    @start_exiftool
    def get_date(self):
        EXIF_DateTimeOriginal = self._exiftool.get_tag('EXIF:DateTimeOriginal', self.path)
        if EXIF_DateTimeOriginal:
            date = datetime.strptime(EXIF_DateTimeOriginal, '%Y:%m:%d %H:%M:%S')
            tz = pytz.timezone(settings.TIME_ZONE)
            local_date = tz.localize(date)
            return local_date
        return None

    def hashfile(self):
        with open(self.path, 'rb') as f:
            return hashfile(f, hashlib.sha256())

    def is_duplicate(self):
        if not self.hash:
            raise MyException('File do not have hash. Fail to decide if its duplicate.')
        if MyFile.objects.filter(hash=self.hash).count():
            return True
        return False

    def copy_to_lib(self):
        '''
        Will generate target path where to place file, copy file,
        change self.path and self.imported_from.
        If file setuated inside media library - it will stay on its place.
        '''
        if self.path.startswith(settings.MEDIA_LIB):
            self.imported_from_path = self.path
            return

        if self.created_date:
            # We have date when file was created. Lets put it into the date folders structure
            subfolders = self.created_date.strftime('%Y/%m-%b/%d')
        else:
            # File with no creation date. Put it to import_date folder
            subfolders = repr(self.imprt)

        target_folder_path = os.path.join(settings.AUTOIMPORT_PATH, subfolders)
        old_folder_path, file_name = os.path.split(self.path)
        target_path = os.path.join(target_folder_path, file_name)
        target_path = maybe_add_number_to_file_name(target_path)
        mkdir_p(target_folder_path)

        shutil.copy(self.path, target_path)
        self.imported_from_path = self.path
        self.path = target_path

    @property
    def dcim_number(self):
        '''Integer found in file name'''
        head, file_name = os.path.split(self.path)
        match = re.match('.*?([0-9]+)\.[a-zA-Z]+', file_name)
        if match:
            return match.group(1)
        return 0

    @property
    def thumb(self):
        if not self._thumb or not os.path.isfile(self._thumb):
            try:
                self.gen_thumbs()
            except MyException as e:
                log.exception(e)
        return self._thumb

    @property
    def preview(self):
        if not self._preview or not os.path.isfile(self._preview):
            try:
                self.gen_thumbs()
            except MyException as e:
                log.exception(e)
        return self._preview

    def del_thumbs(self, save_model=True):
        ''' Remove generated images. '''
        if self._thumb and os.path.isfile(self._thumb):
            os.remove(self._thumb)
            self._thumb = ''
        if self._preview and os.path.isfile(self._preview):
            os.remove(self._preview)
            self._preview = ''

        if save_model:
            self.save()

    def gen_preview(self):
        raise NotImplementedError

    def gen_cache_path(self):
        '''
        Generate file name based on MyFile path and CACHES_PATH.
        It will be the same file_name as original file but with
        path in cache dir.
        '''
        if not os.path.isfile(self.path):
            raise MyException('MyFile.path is not a file')

        file_path_relative_to_lib = os.path.relpath(self.path, settings.MEDIA_LIB)
        return os.path.join(settings.CACHE_PATH, file_path_relative_to_lib)

    @property
    @start_exiftool
    def metadata(self):
        if self.path and os.path.isfile(self.path):
            with self._exiftool as et:
                return et.get_metadata(self.path)
        return None

    def get_pil_im(self):
        raise NotImplementedError

    @start_exiftool
    def gen_thumbs(self):
        '''
        Remove old thumb and make new one.
        '''
        self.del_thumbs()

        if self.path and os.path.isfile(self.path):
            # Make a name for the thumbs
            preview_path = self.gen_cache_path() + '.preview.jpg'
            thumb_path = self.gen_cache_path() + '.thumb.jpg'

            # Be sure directories are created
            mkdir_p(os.path.dirname(thumb_path))

            im = self.get_pil_im()

            try:
                # Fix EXIF orientation
                EXIF_Orientation = self._exiftool.get_tag('EXIF:Orientation', self.path)
                if EXIF_Orientation:
                    if EXIF_Orientation == 3:
                        im = im.rotate(180, expand=True)
                    elif EXIF_Orientation == 6:
                        im = im.rotate(270, expand=True)
                    elif EXIF_Orientation == 8:
                        im = im.rotate(90, expand=True)
            except:
                pass

            # Generate preview
            im.thumbnail(settings.PREVIEW_SIZE, Image.ANTIALIAS)
            im.save(preview_path)
            self._preview = preview_path

            # From preview make thumb
            im = crop_rect(im)
            im.thumbnail(settings.THUMB_SIZE, Image.ANTIALIAS)
            im.save(thumb_path)
            self._thumb = thumb_path

            self.save()


class PhotoFile(MyFile):

    def __str__(self):
        # return 'Photo file (%s) %s %s' % (self.created_date, self.path.decode('utf-8'), self.hash)
        return 'Photo file (%s) %s %s' % (self.created_date, self.path, self.hash)

    def get_pil_im(self):
        return Image.open(self.path)


class VideoFile(MyFile):

    def __str__(self):
        return 'Video file (%s) %s %s' % (self.created_date, self.path, self.hash)

    def get_date(self):
        ATOM_HEADER_SIZE = 8
        # Difference between Unix epoch and QuickTime epoch, in seconds
        EPOCH_ADJUSTER = 2082844800

        # Open file and search for moov item
        f = open(self.path, "rb")
        while True:
            atom_header = f.read(ATOM_HEADER_SIZE)
            if atom_header[4:8] == 'moov':
                break
            else:
                atom_size = struct.unpack(">I", atom_header[0:4])[0]
                f.seek(atom_size - 8, 1)
        # found 'moov', look for 'mvhd' and timestamps
        atom_header = f.read(ATOM_HEADER_SIZE)
        if atom_header[4:8] == 'cmov':
            log.debug('moov atom is compressed in %s' % self.path)
        elif atom_header[4:8] != 'mvhd':
            log.debug('Expected to find "mvhd" header for  %s' % self.path)
        else:
            f.seek(4, 1)
            creation_date = struct.unpack(">I", f.read(4))[0]
            creation_date = datetime.utcfromtimestamp(creation_date - EPOCH_ADJUSTER)
            # modification_date = struct.unpack(">I", f.read(4))[0]
            # modification_date = datetime.utcfromtimestamp(modification_date - EPOCH_ADJUSTER)

            if creation_date.year < 1980:
                return super(VideoFile, self).get_date()

            tz_local = pytz.timezone(settings.TIME_ZONE)

            if self.path.lower().endswith('.mov'):
                # Looks like iPhone is storing UTC date in the movie files
                creation_date_utc = pytz.utc.localize(creation_date)
                return creation_date_utc.astimezone(tz_local)

            return tz_local.localize(creation_date)

        return super(VideoFile, self).get_date()


class RawPhoto(MyFile):
    def __str__(self):
        return 'RAW photo file (%s) %s %s' % (self.created_date, self.path, self.hash)

    def get_pil_im(self):

        # Get preview image from RAW file
        im_data = self._exiftool.execute('-b', '-PreviewImage', self.path)
        return Image.open(StringIO.StringIO(im_data))

        # # Read RAW photo format
        # dcraw = subprocess.Popen([settings.DCRAW_EXE, '-c', '-e', self.path], stdout=subprocess.PIPE)
        # stdout, stderr = dcraw.communicate()

        # im = Image.open(StringIO.StringIO(stdout))
        # im = fix_orientation_exif(im)


class LivePhoto(PhotoFile):
    video = models.OneToOneField(VideoFile, on_delete=models.CASCADE, help_text='Link to the video file for the live part of the photo')

    def __str__(self):
        return 'Live photo (%s) %s + %s %s' % (self.created_date, self.path, self.video.path, self.hash)

class Imprt(models.Model):
    '''
    Model to store list of files imported at once
    '''
    date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag')

    def count_files(self):
        return self.myfiles.count()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        # Affects library folder structure
        return 'import_%i-%s' % (self.id, self.date.strftime('%Y.%m.%d'))


class TagType(models.Model):
    title = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    type = models.ForeignKey(TagType)
    value = models.CharField(max_length=512)

    class Meta:
        unique_together = ('type', 'value')

    def __str__(self):
        return '%s %s' % (str(self.type), self.value)