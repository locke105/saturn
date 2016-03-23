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

import json
import os
import subprocess


'''
Builds ISO9660 versions of OpenStack ConfigDrive v2
for attachment to instances.


Basically we have to mimic the following shell commands:

# inject metadata as JSON into file
cat stuff > /var/lib/saturn/instances/*/config_drive_dir/openstack/latest/meta_data.json

# create the ISO image from the directory
genisoimage -o configdrive.iso /var/lib/saturn/instances/*/config_drive_dir

# optionally clean up
rm -rf /var/lib/saturn/instances/*/config_drive_dir
'''


def build_config_drive(instance_dir, metadata):

    os.makedirs(instance_dir + '/config_dir')

    # config drive fs
    os.makedirs(instance_dir + '/config_dir/openstack/latest')
    os.makedirs(instance_dir + '/config_dir/openstack/2012-08-10')

    with open(instance_dir + '/config_dir/openstack/latest/meta_data.json', 'w') as meta_data_file:
        json.dump(metadata, meta_data_file)

    with open(instance_dir + '/config_dir/openstack/2012-08-10/meta_data.json', 'w') as meta_data_file:
        json.dump(metadata, meta_data_file)

    out_file_path = (instance_dir + '/configdrive.iso')
    genisoimage(out_file=out_file_path,
                in_dir=(instance_dir + '/config_dir'))

    return out_file_path


def genisoimage(out_file, in_dir):
    cmd_list = ['/usr/bin/genisoimage',
                '-volid', 'config-2',
                '-quiet',
                '-J',
                '-r',
                '-o', '%(out_file)s'% {'out_file': out_file},
                '%(in_dir)s' % {'in_dir': in_dir}]
    ret_code = subprocess.check_call(cmd_list)
