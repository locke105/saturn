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

import argparse

import saturn


def create_vm(args):
    raise NotImplementedError


def destroy_vm(args):
    saturn.get_vm(args.instance_id).destroy()


def list_vms(args):
    print '---'
    for vm in saturn.list_vms():
        print '- uuid: %s' % vm.UUIDString()
        print '  name: %s' % vm.name()
        print '  state: %s' % vm.state()


def _parse_args():
    p = argparse.ArgumentParser()
    subp = p.add_subparsers(dest='command')

    boot_p = subp.add_parser('boot')
    boot_p.set_defaults(func=create_vm)

    rm_p = subp.add_parser('rm')
    rm_p.set_defaults(func=destroy_vm)
    rm_p.add_argument('instance_id')

    ls_p = subp.add_parser('ls')
    ls_p.set_defaults(func=list_vms)

    return p.parse_args()


def main():
    args = _parse_args()
    return args.func(args)


if __name__ == '__main__':
    main()
