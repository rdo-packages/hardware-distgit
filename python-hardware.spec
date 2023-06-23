%{?!_licensedir:%global license %%doc}
%{!?upstream_version: %global upstream_version %{version}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order

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
License:        Apache-2.0
URL:            https://pypi.python.org/pypi/hardware

Source0:        https://pypi.io/packages/source/h/hardware/hardware-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  git-core

%description
%{common_desc}


%package -n python3-hardware
Summary:        Hardware detection and classification utilities
Obsoletes: python2-hardware < %{version}-%{release}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
Requires: python3-hardware-detect = %{version}-%{release}
%description -n python3-hardware
%{common_desc}

%package -n python3-hardware-detect
Summary:    Hardware detection and classification utilities
Obsoletes: python2-hardware-detect < %{version}-%{release}

Requires: lshw
Requires: smartmontools
Requires: lldpad
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

%description doc
Documentation for Hardware detection and classification utilities.
%endif

%prep
%autosetup -S git -n hardware-%{upstream_version}
rm -rf *.egg-info

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

sed -i /.*-c{env:TOX_CONSTRAINTS_FILE.*/d tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
%{__python3} setup.py build_sphinx
rm -rf doc/build/html/.buildinfo
%endif

%install
%pyproject_install

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
%{python3_sitelib}/hardware*.dist-info

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog

