======
saturn
======

Saturn is a fast and simple orchestration utility for virtual machines.

It currently only works locally, similar to Vagrant but uses libvirt
and cloud images (QCOW2 image files with cloud-init.)


install
=======

To install saturn and try it out::

  git clone https://github.com/locke105/saturn
  cd saturn

  # install binary package dependencies
  bash tools/setup.sh
  
  # install saturn in development mode (from source)
  pip install -e .


usage
=====

Quickly boot a machine::

  saturn boot 'https://cloud-images.ubuntu.com/trusty/current/trusty-server-cloudimg-amd64-disk1.img'

List currently running::

  saturn ls

Terminate a machine::

  saturn rm <UUID>
