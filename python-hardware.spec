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

BuildRequires:  git-core

%description
%{common_desc}


%package -n python3-hardware
Summary:        Hardware detection and classification utilities
%{?python_provide:%python_provide python3-hardware}
Obsoletes: python2-hardware < %{version}-%{release}

BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-babel
BuildRequires:  python3-pbr
Requires: python3-hardware-detect = %{version}-%{release}
Requires: python3-pbr

%description -n python3-hardware
%{common_desc}

%package -n python3-hardware-detect
Summary:    Hardware detection and classification utilities
%{?python_provide:%python_provide python3-hardware-detect}
Obsoletes: python2-hardware-detect < %{version}-%{release}

Requires: lshw
Requires: smartmontools
Requires: lldpad
Requires: python3-pbr
Requires: python3-pexpect
Requires: ethtool
Requires: pciutils

# Benchmarking is an optional feature
%if 0%{?fedora} || 0%{?rhel} > 7
Recommends: fio
Recommends: sysbench
%else
Requires: fio
Requires: sysbench
%endif


%description -n python3-hardware-detect
%{common_desc}


%if 0%{?with_doc}
%package doc
Summary:    Documentation for Hardware detection and classification utilities
Group:      Documentation

BuildRequires:  python3-sphinx

%description doc
Documentation for Hardware detection and classification utilities.
%endif

%prep
%autosetup -S git -n hardware-%{upstream_version}
rm -rf *.egg-info

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%build
%{py3_build}

%if 0%{?with_doc}
%{__python3} setup.py build_sphinx
rm -rf doc/build/html/.buildinfo
%endif

%install
%{py3_install}

%files -n python3-hardware
%license LICENSE
%doc README.rst
%{python3_sitelib}/hardware/test*
%{python3_sitelib}/hardware/__pycache__

%files -n python3-hardware-detect
%license LICENSE
%doc README.rst
%{_bindir}/hardware-detect
%{python3_sitelib}/hardware/benchmark
%{python3_sitelib}/hardware/*.py*
%{python3_sitelib}/hardware*.egg-info

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog

