%{?!_licensedir:%global license %%doc}
%{!?upstream_version: %global upstream_version %{version}}

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-hardware
Summary:        Hardware detection and classification utilities
Version:        0.17
Release:        6%{?dist}
License:        ASL 2.0
URL:            https://pypi.python.org/pypi/hardware

Source0:        https://pypi.python.org/packages/source/h/hardware/hardware-%{upstream_version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
%endif # if with_python3
BuildRequires:  python-pbr
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  git
Requires: python-hardware-detect = %{version}-%{release}
Requires: python-babel
Requires: python-pandas
Requires: python-pbr


%prep
%autosetup -S git -v -n hardware-%{upstream_version}
rm -rf *.egg-info hardware/tests hardware/cardiff/VMs

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'

%build
%{__python2} setup.py build
%{__python2} setup.py build_sphinx
rm -rf doc/build/html/.buildinfo

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
%endif # with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}


%description
Hardware detection and classification utilities.
Features:
* detect hardware features of a Linux systems:
** RAID
** hard drives
** IPMI
** network cards
** DMI info
** memory settings
** processor features
* filter hardware according to hardware profiles

%if 0%{?with_python3}
%package -n python3-hardware
Summary:        Hardware detection and classification utilities
Group:          Development/Languages
Requires: python3-pbr
Requires: python3-babel
Requires: python3-netaddr
Requires: python3-pexpect

%description -n python3-hardware
Hardware detection and classification utilities.
Features:
* detect hardware features of a Linux systems:
** RAID
** hard drives
** IPMI
** network cards
** DMI info
** memory settings
** processor features
* filter hardware according to hardware profiles
%endif # with_python3

%package detect
Summary:    Hardware detection and classification utilities
Requires: lshw
Requires: smartmontools
Requires: lldpad
Requires: sdparm
Requires: sysbench
Requires: fio
Requires: python-pbr
Requires: python-ipaddr
Requires: python-netaddr
%if 0%{?fedora}
Requires: python-pexpect
%else
Requires: pexpect
%endif
Requires: python-ptyprocess
Requires: ethtool
Requires: pciutils

%description detect
Hardware detection and classification utilities.


%package doc
Summary:    Documentation for Hardware detection and classification utilities
Group:      Documentation

%description doc
Documentation for Hardware detection and classification utilities.


%files
%license LICENSE
%doc README.rst
%{python2_sitelib}/hardware/cardiff
%{_bindir}/hardware-cardiff

%files detect
%license LICENSE
%doc README.rst
%{_bindir}/hardware-detect
%{python2_sitelib}/hardware/benchmark
%{python2_sitelib}/hardware/*.py*
%{python2_sitelib}/hardware*.egg-info

%files doc
%license LICENSE
%doc doc/build/html

%if 0%{?with_python3}
%files -n python3-hardware
%license LICENSE
%doc README.rst
%{python3_sitelib}/hardware*
%endif # with_python3

%changelog
* Thu Feb 11 2016 Frederic Lepied <frederic.lepied@redhat.com> 0.17-6
- split the detect part in a standalone package python-hardware-detect
- fix the missing requires: ethtool and pcitutils

* Wed Feb 10 2016 Frederic Lepied <frederic.lepied@redhat.com> 0.17-5
- exclude examples

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 14 2015 Frederic Lepied <frederic.lepied@redhat.com> 0.17-2
- add missing requires: lshw, smartmontools, lldpad, sdparm (Erwan)
- add missing requires: fio (taken from Delorean)

* Wed Sep 23 2015 Frederic Lepied <frederic.lepied@redhat.com> 0.17-1
- new version (bug #1196176)

* Sat Aug  8 2015 Frederic Lepied <frederic.lepied@redhat.com> 0.16-1
- new version (bug #1196176)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Frederic Lepied <frederic.lepied@redhat.com> - 0.15-1
- new version (bug #1196176)

* Tue May 05 2015 Haïkel Guémar <hguemar@fedoraproject> - 0.14-2
- Fix requirements
- Add a patch to improve output of cardiff from John Trowbridge

* Tue Mar 31 2015 Frederic Lepied <frederic.lepied@redhat.com> - 0.14-1
- new version (bug #1196176)

* Thu Mar 26 2015 Frederic Lepied <frederic.lepied@redhat.com> - 0.13-1
- new version (bug #1196176)

* Wed Mar 18 2015 Frederic Lepied <frederic.lepied@redhat.com> - 0.12-1
- new version (bug #1196176)

* Tue Feb 24 2015 Dmitry Tantsur <divius.inside@gmail.com> - 0.11-1
- new version (bug #1195701)

* Fri Feb 13 2015 Dmitry Tantsur <dtantsur@redhat.com> - 0.9-1
- Initial package build

