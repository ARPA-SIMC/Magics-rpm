%global releaseno 1

Name:           Magics
Version:        4.4.0
Release:        %{releaseno}%{dist}
Summary:        Library and tools to visualize meteorological data and statistics
URL:            http://www.ecmwf.int/products/data/software/magics++.html
Source0:        https://software.ecmwf.int/wiki/download/attachments/3473464/%{name}-%{version}-Source.tar.gz
Patch0:         https://raw.githubusercontent.com/ARPA-SIMC/Magics-rpm/v%{version}-%{releaseno}/magics-fix-warnings.patch
Patch1:         https://raw.githubusercontent.com/ARPA-SIMC/Magics-rpm/v%{version}-%{releaseno}/magics-rm-ksh.patch
Patch2:         https://raw.githubusercontent.com/ARPA-SIMC/Magics-rpm/v%{version}-%{releaseno}/magics-fix-shebangs.patch
License:        Apache License, Version 2.0

BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  cmake
BuildRequires:  qt5-qtbase-devel
BuildRequires:  proj-devel >= 6
BuildRequires:  libgeotiff-devel
BuildRequires:  swig
BuildRequires:  eccodes-devel
BuildRequires:  cairo-devel
BuildRequires:  pango-devel
BuildRequires:  eccodes-data
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
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildRequires:  python3-jinja2
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

%prep
%setup -q -n %{name}-%{version}-Source
%patch0
%patch1
%patch2

%build

mkdir build
pushd build

# the following options are basically to work around travis 4Mb log limit
# and can be safely removed
# (see https://github.com/travis-ci/travis-ci/issues/3865 )
#    -DCMAKE_CXX_FLAGS="$CXXFLAGS -Wno-deprecated-declarations -Wno-unused-local-typedefs"
#    -DCMAKE_INSTALL_MESSAGE=NEVER

cmake .. \
    -DCMAKE_CXX_FLAGS="$CXXFLAGS -Wno-deprecated-declarations -Wno-unused-local-typedefs" \
    -DCMAKE_PREFIX_PATH=%{_prefix} \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_MESSAGE=NEVER \
    -DBUILD_SHARED_LIBS=ON \
    -DINSTALL_LIB_DIR=%{_lib} \
    -DENABLE_CAIRO=ON \
    -DENABLE_GEOTIFF=ON \
    -DENABLE_NETCDF=ON \
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
MAGPLUS_HOME=%{buildroot} CTEST_OUTPUT_ON_FAILURE=1 LD_LIBRARY_PATH=%{buildroot}%{_libdir} ctest
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd build
%make_install

# remove rpath
sed -i 's|^libs=.*$|libs=-L${libdir} -lMagPlus|g' %{buildroot}/%{_libdir}/pkgconfig/magics.pc
sed -i 's|-Wl,-rpath,${libdir}64 ${libdir}64/lib|-l|g' %{buildroot}/%{_libdir}/pkgconfig/magics.pc
sed -i 's|\.so[0-9\.]*||g' %{buildroot}/%{_libdir}/pkgconfig/magics.pc

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
%{_includedir}/magics
%{_libdir}/pkgconfig/magics.pc
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/cmake/magics

%changelog
* Mon Jul 13 2020 Emanuele Di Giacomo <edigiacomo@arpae.it> - 4.4.0-1
- Use new feature of eccodes to display data coded  in various projections
- Improvement in the position of the title for the vertical axis
- Bug Fix in the labelling of the legend (MAGP-1238)

* Fri Jun  5 2020 Daniele Branchini <dbranchini@arpae.it> - 4.3.3-1
- Version 4.3.3, dropping centos 7 support and proj < 6 support

* Wed Feb 26 2020 Daniele Branchini <dbranchini@arpae.it> - 4.2.6-1
- Version 4.2.6

* Wed Jan  8 2020 Daniele Branchini <dbranchini@arpae.it> - 4.2.3-1
- Version 4.2.3

* Thu Nov  7 2019 Daniele Branchini <dbranchini@arpae.it> - 4.2.0-1
- Version 4.2.0

* Thu Sep 19 2019 Daniele Branchini <dbranchini@arpae.it> - 4.1.3-1
- Version 4.1.3

* Fri Jun  7 2019 Emanuele Di Giacomo <edigiacomo@arpae.it> - 4.0.3-2
- Fixed Python shebang of magicsCompatibilityChecker

* Thu May 16 2019 Daniele Branchini <dbranchini@arpae.it> - 4.0.3-1
- Version 4.0.3
- Forced old gfortran compiler to match the eccodes package

* Fri May  3 2019 Daniele Branchini <dbranchini@arpae.it> - 4.0.2-2
- Removed python package since the interface has been separated
- Added CentOs7 dependency for newer gcc

* Wed Apr 10 2019 Daniele Branchini <dbranchini@arpae.it> - 4.0.2-1
- Version 4.0.3

* Wed Jan 23 2019 Daniele Branchini <dbranchini@arpae.it> - 3.3.1-1
- Version 3.3.1

* Wed Nov 28 2018 Daniele Branchini <dbranchini@arpae.it> - 3.2.2-1
- Version 3.2.2, removed perl dependencies (according to ecmwf changelog)

* Tue Oct 16 2018 Daniele Branchini <dbranchini@arpae.it> - 3.2.0-1
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
