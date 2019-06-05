#!/bin/bash
set -exo pipefail

image=$1

if [[ $image =~ ^centos: ]]
then
    pkgcmd="yum"
    builddep="yum-builddep"
    sed -i '/^tsflags=/d' /etc/yum.conf
    yum install -q -y epel-release
    yum install -q -y @buildsys-build
    yum install -q -y yum-utils
    yum install -q -y git
    yum install -q -y rpmdevtools
    yum install -q -y yum-plugin-copr
    yum install -q -y pv
    yum install -q -y centos-release-scl-rh
    yum-config-manager --enable rhel-server-rhscl-7-rpms
    yum install -q -y devtoolset-7
    yum copr enable -q -y simc/stable
elif [[ $image =~ ^fedora: ]]
then
    pkgcmd="dnf"
    builddep="dnf builddep"
    sed -i '/^tsflags=/d' /etc/dnf/dnf.conf
    dnf install -q -y 'dnf-command(builddep)'
    dnf install --allowerasing -q -y @buildsys-build
    dnf install -q -y git
    dnf install -q -y rpmdevtools
    dnf install -q -y pv
    dnf copr enable -q -y simc/stable
fi

$builddep -q -y Magics.spec

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
