virtdc : virtual machine management CLI
=======================================

.. image:: https://drone.io/github.com/dcsolvere/virtdc/status.png
   :target: https://drone.io/github.com/dcsolvere/virtdc
   :alt: drone.io CI build status

.. image:: https://pypip.in/v/virtdc/badge.png
   :target: https://pypi.python.org/pypi/virtdc/
   :alt: Latest PyPI version

.. image:: https://pypip.in/d/virtdc/badge.png
   :target: https://pypi.python.org/pypi/virtdc/
   :alt: Number of PyPI downloads

`virtdc` A high-level Python CLI for virtual machine placement and scaling which provides a way to create, manage and monitor virtual machines effectively.

Pre-requisite
=============
libvirt api is a required pre requisite for this package
Use yum or apt-get::

   $ sudo yum install libvirt


Setup
=====

Use easy_install or pip::

   $ sudo mkdir /var/lib/virtdc
   $ sudo pip install -t /var/lib/virtdc virtdc
   $ sudo cp /var/lib/virtdc/usr_bin/virtdc.py /usr/bin/virtdc

Commands
========
The following are the core functionalities of the virtdc api

create - creates new domain from the base image::

   $virtdc create -h
   usage: virtdc create [-h] vmid cpu memory maxmemory io

   positional arguments:
     vmid        get the vmid
     cpu         get the cpu
     memory      get memory in KiB
     maxmemory   get maximum memory in KiB
     io          get the io in KiB

terminate-terminates the running domain::

   $virtdc terminate -h
   usage: virtdc terminate [-h] vmid

   positional arguments:
     vmid        get the vmid

list-lists running domain in all hosts::

   $virtdc list -h
   usage: virtdc list [-h]

dominfo gives the domain information::

   $virtdc dominfo -h
   usage: virtdc dominfo [-h] vmid

   positional arguments:
     vmid        get the domain id

hostinfo gives the host information::

   $virtdc hostinfo -h
   usage: virtdc hostinfo [-h] hostname

   positional arguments:
     hostname    get the host

force-migrate migrates domain from source host to dest host::

   $virtdc force-migrate -h
   usage: virtdc force-migrate [-h] vmid sourcehost desthost

   positional arguments:
     vmid        get the domain
     sourcehost  get the source host
     desthost    get the dest host
     
removehost-removes the host from the cluster::

   $virtdc removehost -h
   usage: virtdc removehost [-h] hostname

   positional arguments:
     hostname    get the host

addhost-adds new host to the cluster::

   $virtdc addhost  -h
   usage: virtdc addhost [-h] hostname cpu memory io

   positional arguments:
     hostname    get the host
     cpu         get the cpu
     memory      get memory in KiB
     io          get the io in KiB
     
getip-gets domain ip::

   $virtdc getip  -h
   usage: virtdc getip [-h] vmid

   positional arguments:
     vmid        get the domain id

monitorgraph-monitors cpu, memory, io usage::

   $virtdc monitorgraph  -h
   usage: virtdc monitorgraph [-h]

Features
========
* CLI for virtual machine placement and resource scaling based on usage comparison effectively.

Requirements
============
* Python 2.6, 2.7, 3.2, 3.3, 3.4
* setuptools

License
=======
MIT
