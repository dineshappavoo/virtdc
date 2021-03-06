#!/usr/bin/env python


import os
import sys

from os.path import join as pjoin, splitext, split as psplit
from setuptools import setup, find_packages
from distutils.sysconfig import get_python_lib

# Warn if we are installing over top of an existing installation. This can
# cause issues where files that were deleted from a more recent virtdc
overlay_warning = False
if "install" in sys.argv:
    lib_paths = [get_python_lib()]
    if lib_paths[0].startswith("/var/lib/"):
        # We have to try also with an explicit prefix of /usr/local in order to
        # catch Debian's custom user site-packages directory.
        lib_paths.append(get_python_lib(prefix="/var/lib"))
    for lib_path in lib_paths:
        existing_path = os.path.abspath(os.path.join(lib_path, "virtdc"))
        if os.path.exists(existing_path):
            # We note the need for the warning here, but present it after the
            # command is run, so it's more likely to be seen.
            overlay_warning = True
            break


EXCLUDE_FROM_PACKAGES = ['virtdc.packaging']


setup(
      name='virtdc',
      version='0.1.2',
      url='http://dcsolvere.github.io/virtdc/',
      author='Dinesh Appavoo',
      author_email='dinesha.cit@gmail.com',
      description=('A high-level Python  CLI for virtual machine '
                   'placement and scaling which provides a way to '
                   'create, manage and monitor virtual machines effectively'),
      license='MIT',
      packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
      
      package_data = {
      # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.sh'],
      # And include any *.msg files found in the 'hello' package, too:
      'framework': ['*.xml'],
      },
      
      include_package_data=True,

      extras_require={
      "bcrypt": ["bcrypt"],
      },
      zip_safe=False,
      scripts=[pjoin('usr_bin', 'virtdc.py')],
      )


if overlay_warning:
    sys.stderr.write("""
        ========
        WARNING!
        ========
        You have just installed virtdc over top of an existing
        installation, without removing it first. Because of this,
        your install may now include extraneous files from a
        previous version that have since been removed from
        virtdc. This is known to cause a variety of problems. You
        should manually remove the
        %(existing_path)s
        directory and re-install virtdc.
        """ % {"existing_path": existing_path})
