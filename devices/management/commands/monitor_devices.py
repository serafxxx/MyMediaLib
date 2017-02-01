import logging

import pyudev as pyudev
import time
from django.core.management import BaseCommand
from util import mkdir_p

from util import call

log = logging.getLogger(__name__)


class DeviceManager(object):
    def action_add(self):
        raise NotImplementedError
    def action_remove(self):
        raise NotImplementedError

IPHONE_MOUNT_DIR = '/tmp/iPhone'

class IPhone(DeviceManager):
    '''
        Debian requirements
        $sudo apt-get install ideviceinstaller python-imobiledevice libimobiledevice-utils libimobiledevice6 libplist3 python-plist ifuse
    '''

    def __init__(self, id, mount_dir=IPHONE_MOUNT_DIR ):
        self.id = id
        self.mount_dir = mount_dir
        mkdir_p(self.mount_dir)


    def action_add(self):
        if not self.paired():
            self.pair()
        self.mount()

    def action_remove(self):
        self.umount()

    def paired(self):
        '''
        Checks if iPhone was already paired. Calls ```idevicepair list```
        '''
        for id in call('idevicepair', 'list'):
            if id == self.id:
                return True
        return False

    def pair(self):
        lines = call('idevicepair', 'pair')
        log.debug('\n'.join(lines))
        time.sleep(3)

    def unpair(self):
        lines = call('idevicepair', 'unpair')
        log.debug('\n'.join(lines))

    def mount(self):
        lines = call('ifuse', self.mount_dir)
        log.debug('\n'.join(lines))

    def umount(self):
        time.sleep(1)
        lines = call('fusermount', '-u', self.mount_dir)
        log.debug('\n'.join(lines))


# MY_DEVICES = [
#     {
#         'title': 'iPhone Serafim',
#         'mount_dir': '/mnt/iPhone_serafim',
#         'manager': 'IphoneManager',
#         'identity':{
#             'DEVTYPE': 'usb_device',
#             'ID_MODEL': 'iPhone',
#             'ID_SERIAL_SHORT': '64bba78e7c9cc2c0b4d4716795ac2db881627e3c'
#         }
#     }
# ]


class Command(BaseCommand):
    help = 'Monitor devices and start import automatically'

    def add_arguments(self, parser):
        pass
        # Named (optional) arguments
        # parser.add_argument(
        #     '--default',
        #     action='store_true',
        #     dest='default',
        #     default=False,
        #     help='Import files from settings.IMPORT_FROM folders',
        # )

        # parser.add_argument(
        #     '--lib',
        #     action='store_true',
        #     dest='lib',
        #     default=False,
        #     help='Scan settings.MEDIA_LIB and add new files to DB',
        # )
        #
        # parser.add_argument(
        #     '--from',
        #     action='store',
        #     dest='from',
        #
        #     help='Scan designated folder and add new files to DB',
        # )


    def handle(self, *args, **options):

        try:

            context = pyudev.Context()
            monitor = pyudev.Monitor.from_netlink(context)
            monitor.filter_by(subsystem='usb')  # Remove this line to listen for all devices.
            monitor.start()

            for device in iter(monitor.poll, None):

                # for k in device.properties:
                #     log.debug('device.properties[%s] = %s' % (k, device.properties[k]))

                # Filter out usb interfaces etc.
                if device.properties['DEVTYPE'] == 'usb_device':
                    if device.properties['ID_MODEL'] == 'iPhone':
                        log.info('iPhone %s' % device.properties['ID_SERIAL_SHORT'])
                        iphone = IPhone(device.properties['ID_SERIAL_SHORT'])
                        # Wait for dev init to take place
                        time.sleep(1)
                        if device.properties['ACTION'] == 'add':
                            iphone.mount()
                        elif device.properties['ACTION'] == 'remove':
                            iphone.umount()

        except Exception as e:
            log.exception(e)