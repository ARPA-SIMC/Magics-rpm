%if 0%{?rhel} == 7
%define python3_vers python34
%define cmake_vers cmake3
%define ctest_vers ctest3
%else
%define python3_vers python3
%define cmake_vers cmake
%define ctest_vers ctest
%endif

%global releaseno 1

Name:           Magics
Version:        3.2.2
Release:        %{releaseno}%{dist}
Summary:        Library and tools to visualize meteorological data and statistics
URL:            http://www.ecmwf.int/products/data/software/magics++.html
Source0:        https://software.ecmwf.int/wiki/download/attachments/3473464/%{name}-%{version}-Source.tar.gz
Patch0:         https://raw.githubusercontent.com/ARPA-SIMC/Magics-rpm/v%{version}-%{releaseno}/magics-fix-warnings.patch
Patch1:         https://raw.githubusercontent.com/ARPA-SIMC/Magics-rpm/v%{version}-%{releaseno}/magics-rm-ksh.patch
License:        Apache License, Version 2.0

BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  %{cmake_vers}
BuildRequires:  qt5-qtbase-devel
BuildRequires:  proj-devel
BuildRequires:  libgeotiff-devel
BuildRequires:  swig
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
BuildRequires:  fftw-devel
BuildRequires:  boost-devel
BuildRequires:  git
BuildRequires:  %{python3_vers}-devel
BuildRequires:  %{python3_vers}-numpy
BuildRequires:  %{python3_vers}-jinja2
# Apparently only required for CentOs
BuildRequires:  openjpeg2-devel


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
%patch0
%patch1

%build

mkdir build
pushd build

# the following options are basically to work around travis 4Mb log limit
# and can be safely removed
# (see https://github.com/travis-ci/travis-ci/issues/3865 )
#    -DCMAKE_CXX_FLAGS="$CXXFLAGS -Wno-deprecated-declarations -Wno-unused-local-typedefs"
#    -DCMAKE_INSTALL_MESSAGE=NEVER

%{cmake_vers} .. \
    -DCMAKE_CXX_FLAGS="$CXXFLAGS -Wno-deprecated-declarations -Wno-unused-local-typedefs" \
    -DCMAKE_PREFIX_PATH=%{_prefix} \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_MESSAGE=NEVER \
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
# MAGPLUS_HOME is needed for the tests to work, see:
# https://software.ecmwf.int/wiki/display/MAGP/Installation+Guide
MAGPLUS_HOME=%{buildroot} CTEST_OUTPUT_ON_FAILURE=1 LD_LIBRARY_PATH=%{buildroot}%{_libdir} %{ctest_vers}
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd build
%make_install

pushd %{buildroot}%{_libdir}
for l in *.so
do
    mv $l $l.3.0.0
    ln -s $l.3.0.0 $l.3
    ln -s $l.3.0.0 $l
done

popd


%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/magics
%{_libdir}/*.so.3*

%files devel
%defattr(-,root,root)
%{_includedir}/magics/*
%{_libdir}/pkgconfig/magics.pc
%{_libdir}/*.so
%{_libdir}/*.a


%files -n python3-%{name}

%defattr(-,root,root)
%{python3_sitearch}/*

%changelog
* Wed Nov 28 2018 Daniele Branchini <dbranchini@arpae.it> - 3.2.2-1
- Version 3.2.2, removed perl dependencies (according to ecmwf changelog)

* Thu Oct 16 2018 Daniele Branchini <dbranchini@arpae.it> - 3.2.0-1
- Version 3.2.0

* Fri Jul 20 2018 Emanuele Di Giacomo <edigiacomo@arpae.it> - 3.1.0-1
- Version 3.1.0

* Thu Apr 26 2018 Daniele Branchini <dbranchini@arpae.it> - 3.0.3-2
- fixed python tests

* Tue Apr 24 2018 Daniele Branchini <dbranchini@arpae.it> - 3.0.3-1
- Version 3.0.3

* Tue Apr 17 2018 Daniele Branchini <dbranchini@arpae.it> - 3.0.2-1
- Version 3.0.2

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
