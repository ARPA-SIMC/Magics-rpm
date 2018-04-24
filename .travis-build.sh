#!/bin/bash
set -exo pipefail

image=$1

if [[ $image =~ ^centos: ]]
then
    pkgcmd="yum"
    builddep="yum-builddep"
    sed -i '/^tsflags=/d' /etc/yum.conf
    yum install -qy epel-release
    yum install -qy @buildsys-build
    yum install -qy yum-utils
    yum install -qy git
    yum install -qy rpmdevtools
    yum install -qy yum-plugin-copr
    yum install -qy pv
    yum copr enable -qy simc/stable
elif [[ $image =~ ^fedora: ]]
then
    pkgcmd="dnf"
    builddep="dnf builddep"
    sed -i '/^tsflags=/d' /etc/dnf/dnf.conf
    dnf install -qy @buildsys-build
    dnf install -qy 'dnf-command(builddep)'
    dnf install -qy git
    dnf install -qy rpmdevtools
    dnf install -qy pv
    dnf copr enable -qy simc/stable
fi

$builddep -y Magics.spec

if [[ $image =~ ^fedora: || $image =~ ^centos: ]]
then
    pkgname="$(rpmspec -q --qf="Magics-%{version}-%{release}\n" Magics.spec | head -n1)"
    mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
    cp Magics.spec ~/rpmbuild/SPECS/
    spectool -g -R ~/rpmbuild/SPECS/Magics.spec
    set +x
    rpmbuild -ba ~/rpmbuild/SPECS/Magics.spec 2>&1 | pv -q -L 3k
    find ~/rpmbuild/{RPMS,SRPMS}/ -name "${pkgname}*rpm" -exec cp -v {} . \;
    # TODO upload ${pkgname}*.rpm to github release on deploy stage
else
    echo "Unsupported image"
    exit 1
fi
