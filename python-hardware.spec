%{?!_licensedir:%global license %%doc}
%{!?upstream_version: %global upstream_version %{version}}

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
Hardware detection and classification utilities. \
Features: \
* detect hardware features of a Linux systems: \
** RAID \
** hard drives \
** IPMI \
** network cards \
** DMI info \
** memory settings \
** processor features \
* filter hardware according to hardware profiles

Name:           python-hardware
Summary:        Hardware detection and classification utilities
Version:        0.23.0
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://pypi.python.org/pypi/hardware

Source0:        https://pypi.io/packages/source/h/hardware/hardware-%{upstream_version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-setuptools
BuildRequires:  python2-devel
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-six
%endif # if with_python3
BuildRequires:  python2-pbr
BuildRequires:  python2-six
BuildRequires:  python2-sphinx
BuildRequires:  python2-oslo-sphinx
BuildRequires:  git
Requires: numpy
Requires: python-hardware-detect = %{version}-%{release}
Requires: python2-babel
Requires: python2-pandas
Requires: python2-pbr
Requires: python2-six


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
%{common_desc}

%if 0%{?with_python3}
%package -n python3-hardware
Summary:        Hardware detection and classification utilities
Group:          Development/Languages
Requires: python3-numpy
Requires: python3-pbr
Requires: python3-babel
Requires: python3-netaddr
Requires: python3-pexpect
Requires: python3-six

%description -n python3-hardware
%{common_desc}
%endif # with_python3

%package detect
Summary:    Hardware detection and classification utilities
Requires: lshw
Requires: smartmontools
Requires: lldpad
Requires: sdparm
Requires: sysbench
Requires: fio
Requires: python2-pbr
Requires: python-ipaddr
Requires: python2-netaddr
%if 0%{?fedora}
Requires: python2-pexpect
%else
Requires: pexpect
%endif
Requires: python-ptyprocess
Requires: ethtool
Requires: pciutils

%description detect
%{common_desc}


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
* Fri Jan 17 2020 RDO <dev@lists.rdoproject.org> 0.23.0-1
- Update to 0.23.0

