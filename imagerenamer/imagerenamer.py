#!/usr/bin/env python3
#####################################
#    LAST UPDATED     30 JAN 2023   #
#####################################
"""
Renames photos to Year-Month-Day Hour.Minute.Second format
"""
import re
import os
import datetime
import shutil
from PIL import Image
from PIL.ExifTags import TAGS


def main_png(file: str) -> None:
    """
    Used for PNG images with EXIF data
    :param file: Path to a photo to be renamed
    :return: None
    """
    try:
        img = Image.open(file)
        print('Converting {}'.format(file))
        creation_date = re.compile(
            r'<photoshop:DateCreated>(\d)+-(\d)+-(\d)+T(\d)+:(\d)+:(\d)+</photoshop:DateCreated>')
        before_time = 'blah'
        for tag, value in img.info.items():
            match = creation_date.search(str(value))
            if match:
                before_time = match.group()

        no_tags = before_time.replace('<photoshop:DateCreated>', '').replace('</photoshop:DateCreated>', '')
        name = no_tags.replace(':', '.').replace('T', ' ')
        name += '.png'
        img.save('/Volumes/MAC2/Photos/{}'.format(name))
        print('Saved {}'.format(name))
    except ValueError:
        print(f'Skipped {file}')


def main_jpg(file: str) -> None:
    """
    Used for JPG or JPEG images with Photo Month Day, Hour:Minute:Second format
    If it can't determine EXIF date data, it uses the file name to fill
    in the rest of the name and leaves a "Y" for the user to enter the date
    :param file: Path to a photo to be renamed
    :return: None
    """
    image = Image.open(file)
    info = image._getexif()
    time = 'blah'
    try:
        try:
            for tag, value in info.items():
                key = TAGS.get(tag, tag)
                if isinstance(key, str):
                    if key == 'DateTime':
                        time = str(value)
                    elif 'DateTime' in key:
                        time = str(value)
                    else:
                        time = str(file)
        except AttributeError:
            print('Could not rename {} with the year, assuming it is from this year'.format(file))
            filename = file.replace('Photo ', '').replace('.jpg', '')

            if '(1)' in filename:
                time_delta = 1
                filename = filename.replace('(1)', '')
            elif '(2)' in filename:
                time_delta = 3
                filename = filename.replace('(2)', '')
            elif '(3)' in filename:
                time_delta = 3
                filename = filename.replace('(3)', '')
            else:
                time_delta = 0

            time_dt = datetime.datetime.strptime(filename.strip(), '%b %d, %H %M %S %p')

            if time_delta:
                time_dt = time_dt + datetime.timedelta(seconds=time_delta)

            name = '/Volumes/MAC2/Photos/{0}-{1:%m-%d %H.%M.%S}.jpg'.format(datetime.datetime.now().year, time_dt)
        try:
            time_dt = datetime.datetime.strptime(time, '%Y:%m:%d %H:%M:%S')
            name = '/Volumes/MAC2/Photos/{0:%Y-%m-%d %H.%M.%S}.jpg'.format(time_dt)
        except ValueError:
            try:
                print(time)
                time_dt = datetime.datetime.strptime(time, '%b %d, %H %M %S %p')
                name = '/Volumes/MAC2/Photos/{0}-{1:%m-%d %H.%M.%S}.jpg'.format(datetime.datetime.now().year, time_dt)
            except ValueError:
                print('Could not find a year for {}, assuming it is from this year'.format(file))
                filename = file.replace('Photo ', '').replace('.jpg', '')
                time_dt = datetime.datetime.strptime(filename, '%b %d %Y, %H %M %S %p')
                name = '/Volumes/MAC2/Photos/{0}-{1:%m-%d %H.%M.%S}.jpg'.format(datetime.datetime.now().year, time_dt)

        image.save(name)
        print('Saved {}'.format(name))
    except ValueError:
        print(f"Skipped {file}")


def main_heic(file: str) -> None:
    """
    Used for HEIC images with EXIF data
    :param file: Path to a photo to be renamed
    :return: None
    """
    try:
        clean_name = file.replace('Photo ', '').replace('.heic', '').strip()
        try:
            time_dt = datetime.datetime.strptime(clean_name, '%b %d, %H %M %S %p')
        except ValueError:
            time_dt = datetime.datetime.strptime(clean_name, '%Y-%m-%d %H.%M.%S')

        name = '/Volumes/MAC2/Photos/{0}-{1:%m-%d %H.%M.%S}.jpg'.format(datetime.datetime.now().year, time_dt)
        shutil.move(file, name)
        print('Saved {}'.format(name))
    except ValueError:
        print(f'Skipped {file}')


if __name__ == '__main__':
    print('-' * 10, 'Starting', '-' * 10)
    os.chdir('/Users/alex/Library/CloudStorage/Dropbox')
    print('Looking in {}'.format(os.getcwd()))
    ok_filenames = ['JnJ COVID card.jpg', 'JnJ COVID card2.jpg']

    if os.path.exists('/Volumes/MAC2/Photos/'):
        dirs = os.listdir(os.getcwd())
        dirs.sort()
        for pic in dirs:
            if pic.startswith('Photo ') and pic.endswith('.jpg'):
                main_jpg(pic)
                os.unlink(pic)
                print('Deleted {}'.format(pic))
            elif 'IMG_' in pic and pic.endswith('.png'):
                main_png(pic)
                os.unlink(pic)
                print('Deleted {}'.format(pic))
            elif pic.endswith('.png'):
                main_png(pic)
                os.unlink(pic)
                print('Deleted {}'.format(pic))
            elif pic.endswith('.jpg') and pic not in ok_filenames:
                main_jpg(pic)
                # os.unlink(pic)
                # print('Deleted {}'.format(pic))
            elif pic.endswith('.heic'):
                main_heic(pic)
                print('Deleted {}'.format(pic))

        print('-'*10, 'Finished', '-'*10)
    else:
        print('Plug in external drives!')
