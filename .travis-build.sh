#!/bin/bash
set -exo pipefail

image=$1

if [[ $image =~ ^centos:7 ]]
then
    pkgcmd="yum"
    builddep="yum-builddep"
    builddepopt="--disablerepo=centos-sclo-rh"
    sed -i '/^tsflags=/d' /etc/yum.conf
    yum update -q -y
    yum install -q -y epel-release
    yum install -q -y @buildsys-build
    yum install -q -y yum-utils
    yum install -q -y git
    yum install -q -y rpmdevtools
    yum install -q -y yum-plugin-copr
    yum install -q -y pv
    yum install -q -y centos-release-scl-rh
    yum install -q -y devtoolset-7
    yum copr enable -q -y simc/stable
elif [[ $image =~ ^centos:8 ]]
then
    pkgcmd="dnf"
    builddep="dnf builddep"
    builddepopt=""
    sed -i '/^tsflags=/d' /etc/dnf/dnf.conf
    dnf update -q -y
    dnf install -q -y epel-release
    dnf install -q -y 'dnf-command(config-manager)'
    dnf config-manager --set-enabled powertools
    dnf groupinstall -q -y "Development Tools"
    dnf install -q -y 'dnf-command(builddep)'
    dnf install -q -y git
    dnf install -q -y rpmdevtools
    dnf install -q -y pv
    dnf copr enable -q -y simc/stable
    # needed for latest Magics versions
    dnf upgrade -y cmake --disablerepo=\* --enablerepo=appstream --releasever=8-stream --refresh
elif [[ $image =~ ^fedora: ]]
then
    pkgcmd="dnf"
    builddep="dnf builddep"
    builddepopt=""
    sed -i '/^tsflags=/d' /etc/dnf/dnf.conf
    dnf update -q -y
    dnf install -q -y 'dnf-command(builddep)'
    dnf install --allowerasing -q -y @buildsys-build
    dnf install -q -y git
    dnf install -q -y rpmdevtools
    dnf install -q -y pv
    dnf install -q -y 'dnf-command(copr)'
    dnf copr enable -q -y simc/stable
fi

$builddep -q -y $builddepopt Magics.spec

if [[ $image =~ ^fedora: || $image =~ ^centos: ]]
then
    pkgname="$(rpmspec -q --qf="Magics-%{version}-%{release}\n" Magics.spec | head -n1)"
    mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
    cp Magics.spec ~/rpmbuild/SPECS/
    cp *.patch ~/rpmbuild/SOURCES/
    spectool -g -R -S ~/rpmbuild/SPECS/Magics.spec
    set +x
    rpmbuild -ba ~/rpmbuild/SPECS/Magics.spec 2>&1 | pv -q -L 3k
    find ~/rpmbuild/{RPMS,SRPMS}/ -name "${pkgname}*rpm" -exec cp -v {} . \;
    # TODO upload ${pkgname}*.rpm to github release on deploy stage
else
    echo "Unsupported image"
    exit 1
fi
