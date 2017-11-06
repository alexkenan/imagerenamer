#!/usr/bin/env python3.5
#####################################
#    LAST UPDATED     05 NOV 2017   #
#####################################
"""
Renames photos to Year-Month-Day Hour.Minute.Second format
"""
import re
import os
import datetime
from PIL import Image
from PIL.ExifTags import TAGS


def main_png():
    """
    Used for PNG images with EXIF data
    :return: None
    """
    os.chdir('/Volumes/MAC2/Photos/')
    dirs = os.listdir(os.getcwd())
    for file in dirs:
        if 'IMG_' in file and file.endswith('.png'):
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
            img.save(name)
            print('Saved {}'.format(name))
        else:
            print('{} ends with JPG!'.format(file))


def main_jpg():
    """
    Used for JPG or JPEG images with Photo Month Day, Hour:Minute:Second format
    If it can't determine EXIF date data, it uses the file name to fill
    in the rest of the name and leaves a "Y" for the user to enter the date
    :return: None
    """
    print('-'*10, 'Starting', '-'*10)
    os.chdir('/Volumes/MAC2/Photos/')
    dirs = os.listdir(os.getcwd())
    for file in dirs:
        if file.startswith('Photo ') and not file.endswith('.png'):
            print('Converting {}'.format(file))
            image = Image.open(file)
            info = image._getexif()
            time = 'blah'
            for tag, value in info.items():
                key = TAGS.get(tag, tag)
                if key == 'DateTime':
                    time = str(value)
                elif 'DateTime' in key:
                    time = str(value)
            try:
                time_dt = datetime.datetime.strptime(time, '%Y:%m:%d %H:%M:%S')
                name = '{0:%Y-%m-%d %H.%M.%S}.jpg'.format(time_dt)
            except ValueError:
                print('Could not rename {} with the year'.format(file))
                filename = file.replace('Photo ', '').replace('.jpg', '')
                time_dt = datetime.datetime.strptime(filename, '%b %d, %H %M %S %p')
                name = 'Y-{0:%m-%d %H.%M.%S}.jpg'.format(time_dt)

            image.save(name)
            print('Saved {}'.format(name))
        else:
            print('{} ends with PNG, skipping'.format(file))

    print('-'*10, 'Finished', '-'*10)


if __name__ == '__main__':
    main_jpg()
