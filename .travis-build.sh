#!/bin/bash
set -exo pipefail

image=$1

if [[ $image =~ ^centos: ]]
then
    pkgcmd="yum"
    builddep="yum-builddep"
    sed -i '/^tsflags=/d' /etc/yum.conf
    yum update -q -y
    yum install -q -y epel-release
    yum install -q -y @buildsys-build
    yum install -q -y yum-utils
    yum install -q -y git
    yum install -q -y rpmdevtools
    yum install -q -y yum-plugin-copr
    yum install -q -y pv
    yum install -q -y centos-release-scl
    yum install -q -y devtoolset-7
    yum copr enable -q -y simc/stable
elif [[ $image =~ ^fedora: ]]
then
    pkgcmd="dnf"
    builddep="dnf builddep"
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

$builddep -q -y Magics.spec

# Workaround for https://github.com/ARPA-SIMC/Magics-rpm/issues/11
if [[ $image = "fedora:29" ]]
then
    if [ -x /usr/lib64/libQt5Core.so.5 ]; then
        (set -x; strip --remove-section=.note.ABI-tag /usr/lib64/libQt5Core.so.5)
    fi
fi

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
