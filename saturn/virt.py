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

import time
import re

import libvirt



class DomainNotFound(Exception):
    pass


class LibvirtManager(object):

    def __init__(self):
        self.conn = libvirt.open(None)

    def list_domains(self):
        return self.conn.listAllDomains()

    def create_domain(self, xml):
        new_domain = self.conn.defineXML(xml)
        new_domain.create()

        active = False
        while not active:
            try:
                dom = self.find_domain(new_domain.UUIDString())
                active = True if dom.isActive() == 1 else False
            except DomainNotFound:
                time.sleep(0.1)

    def find_domain(self, name_or_id):
        def match_domain(domain):
            if (domain.name() == name_or_id or
                domain.UUIDString() == name_or_id):
                return True
            else:
                return False

        domains = filter(match_domain, self.list_domains())

        if len(domains) > 1:
            raise Exception("Found more than one domain with name: %s" % domain_name)

        if len(domains) == 0:
            raise DomainNotFound()

        return domains[0]


    def destroy_domain(self, name_or_id):
        try:
            domain = self.find_domain(name_or_id)
        except DomainNotFound:
            return

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


def drop_to_interactive():
    import code
    code.interact(local=dict(globals(), **locals()))


def build_state_map():
    symbols = dir(libvirt)
    state_map = {}

    for symbol in symbols:
        match = re.match('^VIR_DOMAIN_([A-Z0-9]+)$', symbol)
        if match is not None:
            state_map[getattr(libvirt, symbol)] = match.group(1)

    return state_map


state_map = build_state_map()
