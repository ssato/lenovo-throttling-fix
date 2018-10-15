from __future__ import absolute_import
import os
import os.path
import setuptools
import setuptools.command.bdist_rpm


NAME = "lenovo_throttling_fix"
DATA_FILES = [("/etc", ["etc/lenovo_throttling_fix.conf"]),
              ("/usr/lib/systemd/system", ["systemd/lenovo_throttling_fix.service"])]


class bdist_rpm(setuptools.command.bdist_rpm.bdist_rpm):
    """Override to use custom RPM SPEC template file.
    """
    def _make_spec_file(self):
        spec = os.path.join(os.curdir, NAME.replace('_', '-') + ".spec")
        return open(spec).readlines()


setuptools.setup(name=NAME,
                 cmdclass=dict(bdist_rpm=bdist_rpm),
                 data_files=DATA_FILES)

# vim:sw=4:ts=4:et:
