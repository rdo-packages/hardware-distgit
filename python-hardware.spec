%{?!_licensedir:%global license %%doc}
%{!?upstream_version: %global upstream_version %{version}}

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-hardware
Summary:        Hardware detection and classification utilities
Version:        XXX
Release:        XXX
License:        ASL 2.0
URL:            https://pypi.python.org/pypi/hardware

Source0:        https://tarballs.openstack.org/hardware/hardware-%{upstream_version}.tar.gz

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
%autosetup -S git -n hardware-%{upstream_version}
rm -rf *.egg-info

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
%{python2_sitelib}/hardware/test*

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
%exclude %{python3_sitelib}/hardware/test*
%endif # with_python3

%changelog
