#!/usr/bin/env python2

# It really should be this simple.
import saturn

# define my request
spec = {'name': 'my_vm_instance',
        'image': 'http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img'}

# request/boot - should throw error if we messed up
my_vm = saturn.boot_vm(spec)

# check status
print 'Status:',
print my_vm.status

# wait for boot/networking etc
my_vm.wait_until(my_vm.ACTIVE)
print 'Running'

# get connection info
net_info = my_vm.network_info
print 'Net Info:',
print net_info

# do something with your VM
#do_stuff(my_vm)

# done now
my_vm.destroy()

# wait until its gone
my_vm.wait_until(my_vm.DELETED)
print 'Destroyed'




# maybe someday
stretch_goals_active = False

if stretch_goals_active:
    # get some metrics for auditing
    total_runtime = my_vm.deleted_at - my_vm.created_at
    print total_runtime
