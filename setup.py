from __future__ import absolute_import
import os.path
from setuptools import setup


PACKAGE = "lenovo_throttling_fix"

DATA_FILES = [("/etc", ["etc/lenovo_throttling_fix.conf"]),
              ("/usr/lib/systemd/system", ["systemd/lenovo_throttling_fix.service"])]


setup(name=PACKAGE,
      include_package_data=True,
      data_files=DATA_FILES)

# vim:sw=4:ts=4:et:
