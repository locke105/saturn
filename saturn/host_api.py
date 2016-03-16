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

import os
import os.path
import shutil
import urllib
import uuid

from saturn import images
from saturn import virt


class HostController(object):

    def __init__(self):
        self.manager = virt.LibvirtManager()
        self.instance_store = InstanceStore()

    def boot_vm(self, vm_spec):
        instance_store_info = self.instance_store.add(vm_spec)

        # build xml and spawn
        domain = Domain(vm_spec)
        domain.add_disk(instance_store_info['image_file_path'])
        self.manager.create_domain(domain.get_xml())

    def delete_vm(self, name_or_id):
        domain = self.manager.find_domain(name_or_id)
        dom_id = domain.UUIDString()

        self.manager.destroy_domain(dom_id)

        # cleanup instance dir
        self.instance_store.remove(dom_id)

    def list_vms(self):
        return self.manager.list_domains()

    def get_vm(self, instance_id):
        return self.manager.find_domain(instance_id)


class InstanceStore(object):

    instance_store_path = '/var/lib/saturn/instances'

    def add(self, vm_spec):
        # build instance dir
        instance_dir = self._get_instance_dir(vm_spec.id)
        os.makedirs(instance_dir + '/images')

        # get image
        image_id = images.store.lookup_by_url(vm_spec.image)
        if not image_id:
            image_id = images.store.add(vm_spec.image)

        images.store.copy(image_id, instance_dir + '/images/disk')

        return {'image_file_path': instance_dir + '/images/disk'}

    def remove(self, instance_id):
        instance_dir = self._get_instance_dir(instance_id)
        if os.path.exists(instance_dir):
            shutil.rmtree(instance_dir)
        else:
            return

    def _get_instance_dir(self, instance_id):
        return os.path.join(self.instance_store_path, str(instance_id))


class VMSpec(object):

    def __init__(self, spec_dict):
        self._spec_dict = spec_dict

        required = ['name', 'image']

        for prop in required:
            setattr(self, prop, spec_dict[prop])

        self.id = str(uuid.uuid4())

    @property
    def orig_spec(self):
        return dict(self._spec_dict)


class Domain(object):
    _base_xml = """
    <domain type="qemu">
      <name>%(domain_name)s</name>
      <uuid>%(uuid)s</uuid>
      <os>
        <type>hvm</type>
        <boot dev='hd'/>
      </os>
      <cpu>
        <topology sockets="1" cores="1" threads="1" />
      </cpu>
      <memory unit="KiB">524288</memory>
      <devices>
        <disk type='file' device='disk'>
          <driver name='qemu' type='qcow2'/>
          <source file='%(disk_file_path)s'/>
          <target dev='sda' bus='%(disk_bus_type)s'/>
        </disk>
        <serial type='pty'>
          <target port='0'/>
        </serial>
        <console type='pty'>
          <target type='serial' port='0'/>
        </console>
        <interface type='network'>
          <source network='default'/>
        </interface>
      </devices>
    </domain>
    """

    def __init__(self, vm_spec):
        self._props = {}
        self._props.update({'domain_name': vm_spec.name,
                            'uuid': vm_spec.id})

    def add_disk(self, disk_file_path):
        self._props.update({'disk_file_path': disk_file_path,
                            'disk_bus_type': self._get_disk_type()})

    def get_xml(self):
        return self._base_xml % self._props

    def _get_disk_type(self):
        #return 'virtio'
        return 'ide'
