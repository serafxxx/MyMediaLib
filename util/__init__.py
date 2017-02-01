import importlib
import logging
from datetime import datetime

import os
import errno
import subprocess
import exifread
import pytz
from django.conf import settings
from PIL import ExifTags

log = logging.getLogger(__name__)

def match_regexp_list(str, regexp_list):
    for regexp in regexp_list:
        if regexp.match(str):
            return True
    return False

def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()

def get_class_from_name(class_name):
    module_name = '.'.join(class_name.split('.')[:-1])
    # Get module object from file_parser_name
    module = importlib.import_module(module_name)
    # Class instance found in the module by class name
    class_instance = getattr(module, class_name.split('.')[-1])
    return class_instance

def maybe_add_number_to_file_name(file_path):
    '''
    Add number to the file name if there is already file with such name
    :param file_path: File path with extension (/path/to/file.ext)
    '''

    if not os.path.isfile(file_path):
        return file_path

    folder_path, file_name = os.path.split(file_path)

    splitted = file_name.split('.')
    file_name_wo_ext = '.'.join(splitted[:-1])
    file_ext = splitted[-1]
    counter = 1
    new_file_name_tpl = '%s-%i.%s'
    new_file_name = new_file_name_tpl % (file_name_wo_ext, counter, file_ext)
    new_file_path = os.path.join(folder_path, new_file_name)
    while os.path.isfile(new_file_path):
        counter += 1
        new_file_name = new_file_name_tpl % (file_name_wo_ext, counter, file_ext)
        new_file_path = os.path.join(folder_path, new_file_name)

    return new_file_path

def mkdir_p(path):
    '''
    Recursivly create missing folders in path
    '''
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise 'Failed to create path %s' % path

def call(cmd, *args):
    # BASE_PATH = os.path.abspath(os.path.dirname(__file__))
    # path = functools.partial(os.path.join, BASE_PATH)
    cmd_list = [cmd] + list(args)
    log.debug(' '.join(cmd_list))
    proc = subprocess.Popen(cmd_list, stdout=subprocess.PIPE)
    proc.wait()
    lines = [line.strip() for line in proc.stdout.readlines() if line != '\n']
    return lines

# def get_date_exif(file_path):
#     with open(file_path, 'rb') as f:
#         tags = exifread.process_file(f, details=False, stop_tag='DateTimeOriginal')
#     tag = tags.get('EXIF DateTimeOriginal')
#
#     # Pillow way
#     # tag = self.image._getexif().get(36867)
#
#     if tag:
#         date = datetime.strptime(tag.values, '%Y:%m:%d %H:%M:%S')
#         tz = pytz.timezone(settings.TIME_ZONE)
#         local_date = tz.localize(date)
#         return local_date
#
#     return None

# def fix_orientation_exif(im):
#     '''Rotate image based on EXIF orientation tags'''
#     for orientation in ExifTags.TAGS.keys():
#         if ExifTags.TAGS.get(orientation) == 'Orientation': break
#     exif = im._getexif()
#     if exif:
#         exif = dict(exif.items())
#
#         if exif.get(orientation) == 3:
#             im = im.rotate(180, expand=True)
#         elif exif.get(orientation) == 6:
#             im = im.rotate(270, expand=True)
#         elif exif.get(orientation) == 8:
#             im = im.rotate(90, expand=True)
#     return im

def crop_rect(im):
    '''Crop image to rectangular size'''
    x, y = im.size
    size = x if x <= y else y
    x_padding = (x - size) / 2
    y_padding = (y - size) / 2
    return im.crop((x_padding, y_padding, x - x_padding, y - y_padding))