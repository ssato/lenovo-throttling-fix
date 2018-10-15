from __future__ import absolute_import
import os
import os.path
import setuptools.command.bdist_rpm
from setuptools import setup


DATA_FILES = [("/etc", ["etc/lenovo_throttling_fix.conf"]),
              ("/usr/lib/systemd/system", ["systemd/lenovo_throttling_fix.service"])]


class bdist_rpm(setuptools.command.bdist_rpm.bdist_rpm):
    """Override to use custom RPM SPEC template file.
    """
    def _make_spec_file(self):
        return open(os.path.join(os.curdir,
                    "lenovo-throttling-fix.spec")).readlines()


setup(cmdclass=dict(bdist_rpm=bdist_rpm),
      data_files=DATA_FILES)

# vim:sw=4:ts=4:et:
