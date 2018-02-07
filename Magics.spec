%if 0%{?rhel} == 7
%define python3_vers python34
%else
%define python3_vers python3
%endif

Name:           Magics
Version:        3.0.0
Release:        1%{dist}
Summary:        Library and tools to visualize meteorological data and statistics
URL:            http://www.ecmwf.int/products/data/software/magics++.html
Source0:        https://software.ecmwf.int/wiki/download/attachments/3473464/%{name}-%{version}-Source.tar.gz
License:        Apache License, Version 2.0

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  qt5-devel
BuildRequires:  proj-devel
BuildRequires:  libgeotiff-devel
BuildRequires:  swig
BuildRequires:  perl-XML-Parser
BuildRequires:  eccodes-devel
BuildRequires:  cairo-devel
BuildRequires:  pango-devel
BuildRequires:  eccodes-devel
BuildRequires:  libemos
BuildRequires:  pkgconfig
BuildRequires:  expat
BuildRequires:  netcdf-devel
BuildRequires:  netcdf-cxx-devel
BuildRequires:  jasper-devel
BuildRequires:  gd-devel
BuildRequires:  boost-devel
BuildRequires:  %{python3_vers}-devel
BuildRequires:  %{python3_vers}-numpy



%description
Runtime files for Magics - 
The library and tools to visualize meteorological data and statistics

Magics is the latest generation of the ECMWF\'s
Meteorological plotting software MAGICS. Although completely
redesigned in C++, it is intended to be as backwards-compatible as
possible with the Fortran interface. The contour package was rewritten
and no longer depends on the CONICON licence.

Besides its programming interfaces (Fortran and C), Magics offers
MagML, a plot description language based on XML aimed at automatic web
production.

The library supports the plotting of contours, wind fields,
observations, satellite images, symbols, text, axis and graphs
(including boxplots).

Data fields to be plotted may be presented in various formats, for
instance GRIB 1 and 2 code data, Gaussian grid, regularly spaced grid
and fitted data. Input data can also be in BUFR and NetCDF format or
retrieved from an ODB database.

The produced meteorological plots can be saved in various formats,
such as PostScript, EPS, PDF, GIF, PNG, SVG and KML.

%package devel
Summary:        Developing package for Magics

%description devel
Header and library files for Magics - The library and tools to visualize meteorological data and statistics

%package -n python3-%{name}
Summary:        Magics Python library
Requires:       %{name} = %{?epoch:%epoch:}%{version}-%{release}
Requires:       numpy

%description -n python3-%{name}
Python modules for Magics - The library and tools to visualize meteorological data and statistics

%prep
%setup -q -n %{name}-%{version}-Source

%build

mkdir build
pushd build

%cmake .. \
    -DCMAKE_PREFIX_PATH=%{_prefix} \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DINSTALL_LIB_DIR=%{_lib} \
    -DBUILD_SHARED_LIBS=ON \
    -DENABLE_CAIRO=ON \
    -DENABLE_GEOTIFF=ON \
    -DENABLE_NETCDF=ON \
    -DENABLE_BUFR=ON \
    -DENABLE_PYTHON=ON \
    -DENABLE_FORTRAN=ON \
    -DENABLE_METVIEW=ON \
    -DGEOTIFF_INCLUDE_DIR=/usr/include/libgeotiff \
    -DENABLE_ODB=OFF \
    -DENABLE_PYTHON=ON \
    -DPYTHON_EXECUTABLE=%{__python3}

%{make_build}
popd

%check
pushd build
make test
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd build
%make_install
popd


%files
%defattr(-,root,root)
%{_bindir}/magml
%{_bindir}/magmlx
%{_bindir}/magjson
%{_bindir}/magjsonx
%{_bindir}/magicsCompatibilityChecker
%{_bindir}/metgram
%{_bindir}/metgram.sh
%{_bindir}/metgramx
%{_datadir}/magics

%files devel
%defattr(-,root,root)
%{_includedir}/magics/*
%{_libdir}/pkgconfig/magics.pc
%{_libdir}/libMagPlus.so
%{_libdir}/libMagPlusDouble.so
%{_libdir}/libMagPlusSingle.so
%{_libdir}/libMagWrapper.a


%files -n python3-%{name}

%defattr(-,root,root)
%{python3_sitearch}/*

%changelog
* Wed Feb  7 2018 Emanuele Di Giacomo <edigiacomo@arpae.it> - 3.0.0-1
- Version 3.0.0

* Thu Jun 30 2016 Daniele Branchini <dbranchini@arpae.it> - 2.29.2-1
- Pacchettizzazione nuova versione per f24

* Tue Nov 4 2014 Daniele Branchini <dbranchini@arpa.emr.it> - 2.22.7-1
- Pacchettizzazione versione cmake

* Wed Jul 14 2010 Daniele Branchini <dbranchini@linus> - 2.10.0-1
- Pacchettizzazione fedora 12

* Tue Jul 14 2009 root <root@localhost.localdomain> - 2.6.4-2
- enabled python and bufr
