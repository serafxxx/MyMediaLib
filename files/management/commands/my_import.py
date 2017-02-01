import logging
import os
from datetime import datetime

import pytz
from django.conf import settings
from django.core.management import BaseCommand

from files.models import MyFile, Imprt, TagType, Tag
from util import match_regexp_list, get_class_from_name
from util.exiftool import ExifTool

log = logging.getLogger(__name__)


def restore_dates_by_dcim_number(myfiles):
    '''
    Will sort files by number and suggest
    created date for those who miss it.
    Will change objects inplace
    '''
    sorted_by_dcim = sorted(myfiles, key=lambda f: f.dcim_number)

    # Initial date (in case all files in import wouldn't have created_date
    date = datetime.now(tz=pytz.utc)

    for myfile in sorted_by_dcim:
        if not myfile.created_date:
            # Set suggested date
            myfile.created_date = date
        else:
            # Update date. So file with no created date will
            # have same created date as previous file in list
            date = myfile.created_date

def process_livephotos(myfiles):
    '''
    Go through the list and try to find pairs of photo-video files which
    forms LivePhoto introduced by Apple.
    Live Photo consists of photo file and video file with same name (minus extension)
    and same date.
    '''

    for file in myfiles:
        file_path_no_ext = ''.join(file.path.split('.')[:-1])
        print file_path_no_ext


def import_folder(folder_path):
    imported_files = []
    imported_hashes = []
    unknown_files = []
    ignored_files = []
    duplicate_files = []

    imprt = Imprt()
    imprt.save()

    counter_total = 0

    # Make an instance of ExifTool for batch file processing
    exiftool = ExifTool(executable_=settings.EXIFTOOL_PATH)
    exiftool.start()

    try:
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                counter_total += 1
                file_path = os.path.join(root, file_name)
                if file_path.startswith(settings.MML_PATH):
                    # Do not import files from system folder
                    continue

                if match_regexp_list(file_name, settings.IGNORE_FILE_PATTERNS):
                    f = MyFile(path=file_path)
                    ignored_files.append(f)
                    log.debug('Ignoring file: %s' % f)
                else:

                    found = False
                    for file_parser_name, extensions in settings.FILE_PARSERS.iteritems():
                        # Iterate through file parsers
                        if file_name.lower().endswith(extensions):
                            # If extension matched

                            # Class instance
                            parser_cls = get_class_from_name(file_parser_name)

                            # File instance
                            f = parser_cls(path=file_path, imprt=imprt)
                            # Pass running ExifTool instance into the object
                            f.set_exiftool(exiftool)
                            f.created_date = f.get_date()
                            f.hash = f.hashfile()

                            found = True

                            log.debug('Found: %s' % f)

                            # Check for duplicates in db and in current import
                            if not f.is_duplicate() and f.hash not in imported_hashes:
                                # f.copy_to_lib()
                                # f.save()
                                imported_files.append(f)
                                imported_hashes.append(f.hash)
                            else:
                                duplicate_files.append(f)
                                log.debug('Skipping duplicate: %s' % f)

                    if not found:
                        # Unknown file type
                        f = MyFile(path=file_path)
                        unknown_files.append(f)
                        log.warning('Unknown file: %s' % f)

        # Fill missed dates and move files to lib
        restore_dates_by_dcim_number(imported_files)
        for f in imported_files:
            f.copy_to_lib()
            f.save()
            log.debug('Imported: %s' % f)

        log.info(
            '%s Total:%i, Imported:%i, Unknown:%i, Duplicates:%i, Ignored:%i' %
            (str(imprt), counter_total, len(imported_files), len(unknown_files), len(duplicate_files), len(ignored_files))
        )

        log.info('Generating thumbnails...')
        for f in imported_files:
            try:
                f.gen_thumbs()
            except:
                pass

        if not imprt.count_files():
            # If nothing was imported remove imprt object
            imprt.delete()
            return None
        return imprt

    finally:
        exiftool.terminate()


class Command(BaseCommand):
    help = 'Import media files to the lib'

    def add_arguments(self, parser):

        # Named (optional) arguments
        # parser.add_argument(
        #     '--default',
        #     action='store_true',
        #     dest='default',
        #     default=False,
        #     help='Import files from settings.IMPORT_FROM folders',
        # )

        parser.add_argument(
            '--lib',
            action='store_true',
            dest='lib',
            default=False,
            help='Scan settings.MEDIA_LIB and add new files to DB',
        )

        parser.add_argument(
            '--from',
            action='store',
            dest='from',

            help='Scan designated folder and add new files to DB',
        )

        parser.add_argument(
            '--imported-from-device',
            action='store',
            dest='imported_from_device',
            help='Set device tag to imprt object',
        )

    def handle(self, *args, **options):

        try:
            # if options['default']:
            #     log.debug('Starting import from settings.IMPORT_FROM..')
            #     for folder_path in settings.IMPORT_FROM:
            #
            #         if not os.path.exists(folder_path):
            #             log.warning('Not existent IMPORT_FROM folder: %s' % folder_path)
            #             continue
            #
            #         log.debug('Importing %s' % folder_path)
            #         imprt = import_folder(folder_path)

            if options['lib']:
                log.debug('Starting import from settings.MEDIA_LIB..')

                if not os.path.exists(settings.MEDIA_LIB):
                    log.warning('Not existent MEDIA_LIB folder: %s' % settings.MEDIA_LIB)
                    return

                imprt = import_folder(settings.MEDIA_LIB)

            if options['from']:
                folder_path = options['from'].decode('utf-8')
                if not os.path.exists(folder_path):
                    log.warning('Not existent folder: %s' % folder_path)
                    return
                log.debug('Starting import from %s' % folder_path)
                imprt = import_folder(folder_path)

            # if imprt:
            #     # We imported something
            #     if options['imported_from_device']:
            #         tag_type, created = TagType.objects.get_or_create(title='Device')
            #         try:
            #             tag = Tag.objects.get(
            #                 type=tag_type,
            #                 value__iexact=options['imported_from_device']
            #             )
            #         except:
            #             tag = Tag(
            #                 type=tag_type,
            #                 value=options['imported_from_device']
            #             )
            #             tag.save()
            #         imprt.tags.add(tag)

        except Exception as e:
            log.exception(e)
