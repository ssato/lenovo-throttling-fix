%global pname   lenovo_throttling_fix
%global debug_package %{nil}
%global gittag  0.3-ss2-RELEASE

%if 0%{?fedora} || 0%{?rhel} > 7 || 0%{?epel} > 7
%bcond_without python3
%else
%bcond_with    python3
%endif

Name:           lenovo-throttling-fix
Summary:        Linux throttling fixes for Lenovo notebooks
Version:        0.3
Release:        ss2%{?dist}
Group:          Applications/Editors
License:        MIT
# Original upstream
#URL:            https://github.com/erpalma/lenovo-throttling-fix/
# Use the following instead of the upstream because I modified a lot.
URL:            https://github.com/ssato/lenovo-throttling-fix/
Source0:        %{url}/archive/%{gittag}/%{pname}-%{version}.tar.gz
# TODO: Find out real runtime depdendencies.
Requires:       dbus-glib
Requires:       gobject-introspection
%if %{with python3}
Requires:       python3-dbus
Requires:       python3-gobject
Requires:       python3-psutil
%else
Requires:       dbus-python
Requires:       python-gobject
# It's available from EPEL7.
Requires:       python2-psutil
%endif
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires:  dbus-glib-devel
BuildRequires:  gobject-introspection-devel
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%else
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif
# ..seealso:: https://github.com/erpalma/lenovo-throttling-fix#thermald
Conflicts:      thermald
%{?systemd_requires}
# It only works on Lenovo notebooks (x86_64 only).
ExclusiveArch:  x86_64

%description
A workaround for Linux throttling issues on Lenovo T480 / T480s / X1C6
notebooks as described at
https://www.reddit.com/r/thinkpad/comments/870u0a/t480s_linux_throttling_bug/.

This forces the CPU package power limit (PL1/2) to 44 W (29 W on battery) and
the temperature trip point to 95 'C (85 'C on battery) by overriding default
values in MSR and MCHBAR every 5 seconds (30 on battery) to block the Embedded
Controller from resetting these values to default.

%prep
%autosetup -n %{pname}-%{version}

%build
%if %{with python3}
%py3_build
%else
%py2_build
%endif

%install
%if %{with python3}
%py3_install
%else
%py2_install
# Dirty hack to install executable script for EPEL7.
test -x %{buildroot}/usr/bin/%{pname} || {
install -d %{buildroot}/usr/bin
cat << EOF > %{buildroot}/usr/bin/%{pname}
#!/usr/bin/python
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('lenovo-throttling-fix', 'console_scripts', 'lenovo_throttling_fix')()
        )
EOF
chmod +x %{buildroot}/usr/bin/%{pname}
}
%endif

%post
%systemd_post lenovo_throttling_fix.service

%preun
%systemd_preun lenovo_throttling_fix.service

%postun
%systemd_postun_with_restart lenovo_throttling_fix.service

%files 
%doc README.md
%{_bindir}/*
%{_sysconfdir}/*
%{_unitdir}/*
%if %{with python3}
%{python3_sitelib}/*
%else
%{python2_sitelib}/*
%endif

%changelog
* Mon Oct 15 2018 Satoru SATOH <satoru.satoh@gmail.com> - 0.3-ss2
- add dirty hacks to build it for EPEL7
- some more minor packaging cleanups and changes

* Mon Oct 15 2018 Satoru SATOH <satoru.satoh@gmail.com> - 0.3-ss1
- some minor packaging cleanups
- change revision

* Sun Sep 30 2018 Satoru SATOH <satoru.satoh@gmail.com> - 0.3-1
- Initial packaging
