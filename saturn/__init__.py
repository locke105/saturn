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

from saturn import host_api


class Instance(object):
    DELETED = 0
    ACTIVE = 1

    def __init__(self, instance_id):
        self.id = instance_id

    @property
    def status(self):
        return None

    @property
    def network_info(self):
        pass

    def wait_until(self, state, timeout=0):
        pass

    def destroy(self):
        host_api.HostController().delete_vm(self.id)


def boot_vm(instance_spec):
    # validate and transform
    spec = host_api.VMSpec(instance_spec)

    host = host_api.HostController()
    host.boot_vm(spec)

    return Instance(spec.id)


def list_vms():
    host = host_api.HostController()
    return host.list_vms()


def get_vm(instance_id):
    return Instance(instance_id)
