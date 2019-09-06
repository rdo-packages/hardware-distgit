# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{?!_licensedir:%global license %%doc}
%{!?upstream_version: %global upstream_version %{version}}

%global with_doc 1

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
Version:        XXX
Release:        XXX
License:        ASL 2.0
URL:            https://pypi.python.org/pypi/hardware

Source0:        https://pypi.io/packages/source/h/hardware/hardware-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  git

%description
%{common_desc}


%package -n python%{pyver}-hardware
Summary:        Hardware detection and classification utilities
%{?python_provide:%python_provide python%{pyver}-hardware}
%if %{pyver} == 3
Obsoletes: python2-hardware < %{version}-%{release}
%endif

BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-six
%if %{pyver} == 3
Requires: python%{pyver}-numpy
%else
Requires: numpy
%endif
Requires: python%{pyver}-hardware-detect = %{version}-%{release}
Requires: python%{pyver}-babel
Requires: python%{pyver}-pandas
Requires: python%{pyver}-pbr
Requires: python%{pyver}-six

%description -n python%{pyver}-hardware
%{common_desc}

%package -n python%{pyver}-hardware-detect
Summary:    Hardware detection and classification utilities
%{?python_provide:%python_provide python%{pyver}-hardware-detect}
%if %{pyver} == 3
Obsoletes: python2-hardware-detect < %{version}-%{release}
%endif

Requires: lshw
Requires: smartmontools
Requires: lldpad
Requires: sysbench
Requires: fio
Requires: python%{pyver}-pbr
Requires: python%{pyver}-netaddr
Requires: python%{pyver}-pexpect
Requires: python%{pyver}-ptyprocess
Requires: ethtool
Requires: pciutils

# Handle python2 exception
%if %{pyver} == 2
Requires: python-ipaddress
%endif

%description -n python%{pyver}-hardware-detect
%{common_desc}


%if 0%{?with_doc}
%package doc
Summary:    Documentation for Hardware detection and classification utilities
Group:      Documentation

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-oslo-sphinx

%description doc
Documentation for Hardware detection and classification utilities.
%endif

%prep
%autosetup -S git -n hardware-%{upstream_version}
rm -rf *.egg-info

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{pyver_bin}|'

%build
%{pyver_build}

%if 0%{?with_doc}
%{pyver_bin} setup.py build_sphinx
rm -rf doc/build/html/.buildinfo
%endif

%install
%{pyver_install}

%files -n python%{pyver}-hardware
%license LICENSE
%doc README.rst
%{pyver_sitelib}/hardware/cardiff
%{_bindir}/hardware-cardiff
%{pyver_sitelib}/hardware/test*
%if %{pyver} == 3
%{pyver_sitelib}/hardware/__pycache__
%endif

%files -n python%{pyver}-hardware-detect
%license LICENSE
%doc README.rst
%{_bindir}/hardware-detect
%{pyver_sitelib}/hardware/benchmark
%{pyver_sitelib}/hardware/*.py*
%{pyver_sitelib}/hardware*.egg-info

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
