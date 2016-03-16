#  Copyright (C) 2016 Mathew Odden
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import hashlib
import os
import json
import os.path
import shutil
import urllib
import urlparse


def canonicalize_image_id(image_id):
    return hashlib.sha1(image_id).hexdigest()


class ImageStore(object):

    images_dir = '/var/lib/saturn/images'

    def add(self, image_url):
        image_hash = canonicalize_image_id(image_url)
        image_dir = self.images_dir + '/%s' % image_hash

        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        metadata = {'image_id': image_hash,
                    'image_url': image_url,
                    'state': 'downloading'}
        with open(image_dir + '/json', 'w') as metadata_file:
            json.dump(metadata, metadata_file)

        if not os.path.exists(image_dir + '/disk'):
            urllib.urlretrieve(image_url, image_dir + '/disk.part')
            os.rename(image_dir + '/disk.part', image_dir + '/disk')

        metadata = {'image_id': image_hash,
                    'image_url': image_url,
                    'state': 'ready'}
        with open(image_dir + '/json', 'w') as metadata_file:
            json.dump(metadata, metadata_file)

        return image_hash

    def remove(self, image_dir):
        full_image_dir = os.path.join(self.images_dir, image_dir)
        if os.path.exists(full_image_dir):
            shutil.rmtree(full_image_dir)

    def get(self, image_id):
        return Image._unmarshal_from_dir(self.images_dir + '/' + image_id)

    def copy(self, image_id, to_path):
        image = self.get(image_id)
        shutil.copy(self.images_dir + '/' + image.image_id + '/disk', to_path)

    def lookup_by_url(self, image_url):
        id_hash = canonicalize_image_id(image_url)

        images = filter(lambda x: x == id_hash, self.list())

        if images and len(images) == 1:
            return images[0]
        else:
            return None

    def list(self):
        images = []
        for entry in os.listdir(self.images_dir):
            images.append(entry)
        return images


class Image(object):

    @staticmethod
    def _unmarshal_from_dir(image_path):
        if not os.path.exists(image_path):
            metadata = {'state': 'deleted'}

        if not os.path.exists(image_path + '/json'):
            metadata = {'state': 'corrupted'}
        else:
            with open(image_path + '/json') as metadata_file:
                metadata = json.load(metadata_file)

        image_id = os.path.basename(image_path)

        img = Image(image_id=image_id)
        img.__dict__.update(metadata)
        return img

    def __init__(self, image_id):
        self.image_id = image_id

store = ImageStore()
