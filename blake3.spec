# Copyright 2026 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

%global __strip /bin/true

%define _use_internal_dependency_generator 0
%define __find_requires %{nil}
%global __spec_install_post \
    /usr/lib/rpm/check-rpaths \
    /usr/lib/rpm/check-buildroot \
    /usr/lib/rpm/brp-compress

%undefine _build_create_debug
%define __arch_install_post export NO_BRP_STRIP_DEBUG=true NO_BRP_AR=true

Name: blake3
Epoch: 100
Version: 1.8.3
Release: 1%{?dist}
Summary: Official C implementation of the BLAKE3 cryptographic hash function
License: Apache-2.0
URL: https://github.com/BLAKE3-team/BLAKE3/tags
Source0: %{name}_%{version}.orig.tar.gz
%if 0%{?rhel} == 9
BuildRequires: gcc-toolset-15
BuildRequires: gcc-toolset-15-gcc
BuildRequires: gcc-toolset-15-gcc-c++
BuildRequires: gcc-toolset-15-libasan-devel
BuildRequires: gcc-toolset-15-libatomic-devel
BuildRequires: gcc-toolset-15-libstdc++-devel
BuildRequires: gcc-toolset-15-libubsan-devel
%endif
BuildRequires: cmake4
BuildRequires: gcc-c++
BuildRequires: tbb-devel

%description
BLAKE3 is a cryptographic hash function with features like Extendable
Output Function (XOF), Key Derivation Functions (KDF), Pseudorandom
Functions (PRF) and Keyed Hashes (MAC). It introduces a Merkle tree
structure that enables parallel computation across multiple cores.
BLAKE3 offers a fixed 256-bit output and targets memory efficiency.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%if 0%{?rhel} == 9
. /opt/rh/gcc-toolset-15/enable
%endif
pushd c && \
    cmake \
        . \
        -DBLAKE3_USE_TBB="ON" \
        -DBUILD_SHARED_LIBS=ON \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr && \
popd
pushd c && \
    cmake \
        --build . \
        --parallel 10 \
        --config Release && \
    popd

%install
pushd c && \
    export DESTDIR=%{buildroot} && \
    cmake \
        --install . && \
popd

%check

%if 0%{?suse_version} >= 1500
%package -n libblake3-0
Summary: A cryptographic hash function

%description -n libblake3-0
BLAKE3 is a cryptographic hash function with features like Extendable
Output Function (XOF), Key Derivation Functions (KDF), Pseudorandom
Functions (PRF) and Keyed Hashes (MAC). It introduces a Merkle tree
structure that enables parallel computation across multiple cores.
BLAKE3 offers a fixed 256-bit output and targets memory efficiency.

%package devel
Summary: Development files for libblake3
Requires: libblake3-0 = %{epoch}:%{version}-%{release}

%description devel
This package contains the development files (mainly C header files) for libblake3.

%post -n libblake3-0 -p /sbin/ldconfig
%postun -n libblake3-0 -p /sbin/ldconfig

%files -n libblake3-0
%license LICENSE_A2
%{_libdir}/libblake3.so.*

%files devel
%license LICENSE_A2
%{_includedir}/blake3.h
%{_libdir}/cmake/blake3
%{_libdir}/libblake3.so
%{_libdir}/pkgconfig/libblake3.pc
%endif

%if !(0%{?suse_version} >= 1500)
%package devel
Summary: Development files for libblake3
Requires: blake3 = %{epoch}:%{version}-%{release}

%description devel
Development files for the blake3 library.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE_A2
%{_libdir}/libblake3.so.*

%files devel
%license LICENSE_A2
%{_includedir}/blake3.h
%{_libdir}/cmake/blake3
%{_libdir}/libblake3.so
%{_libdir}/pkgconfig/libblake3.pc
%endif

%changelog
