#!/usr/bin/env python2

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

import libvirt


def print_domains():
    conn = libvirt.openReadOnly(None)

    domains = conn.listDomainsID()

    for domain in domains:
        print domains


class LibvirtManager(object):

    def __init__(self):
        self.conn = libvirt.open(None)

    def list_domains(self):
        return self.conn.listAllDomains()

    def create_domain(self, domain_name):
        xml = """
        <domain type="qemu">
          <name>%(domain_name)s</name>
          <os>
            <type>hvm</type>
            <boot dev='hd'/>
          </os>
          <cpu>
            <topology sockets="1" cores="1" threads="1" />
          </cpu>
          <memory unit="KiB">524288</memory>
        </domain>
        """
        new_domain = self.conn.defineXML(xml % {'domain_name': domain_name})
        new_domain.create()

    def destroy_domain(self, domain_name):
        domain = filter(lambda x: x.name() == domain_name, self.list_domains())

        if len(domain) > 1:
            raise Exception("Found more than one domain with name: %s" % domain_name)

        if len(domain) == 0:
            # nothing to destroy...?
            return

        domain = domain[0]

        # remove persistence
        domain.undefine()
        # force shutdown
        domain.destroy()

    def info_dict(self):
        # these must be domain specific or something...
        #    'getCPUModelNames',
        #    'getCPUStats',
        #    'getCellsFreeMemory',
        #    'getFreeMemory',
        #    'getMaxVcpus',
        #    'getMemoryStats',
        whitelist = [
            'getCPUMap',
            'getCapabilities',
            'getHostname',
            'getInfo',
            'getLibVersion',
            'getMemoryParameters',
            'getSecurityModel',
            'getSysinfo',
            'getType',
            'getURI',
            'getVersion',
        ]
        props = {}
        for method in whitelist:
            if method.startswith('get'):
                props[method[3:]] = getattr(self.conn, method)()

        return props



def print_connection_info(conn):

    manager = LibvirtManager()
    import pprint

    pprint.pprint(manager.info_dict())


def quick_test():
    LibvirtManager().create_domain('testdomain')
    LibvirtManager().destroy_domain('testdomain')


def drop_to_interactive():
    import code
    code.interact(local=dict(globals(), **locals()))

if __name__ == '__main__':
    print_connection_info(None)
