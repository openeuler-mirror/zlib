Name:             zlib
Version:          1.2.12
Release:          1
Summary:          A lossless data-compression library
License:          zlib and Boost
URL:              http://www.zlib.net
Source0:          http://www.zlib.net/zlib-%{version}.tar.gz

# Patch0 get from fedora
Patch0:           zlib-1.2.5-minizip-fixuncrypt.patch
%ifarch aarch64
# Patch1 to Patch3 get from http://www.gildor.org/en/projects/zlib
Patch1:           0001-Neon-Optimized-hash-chain-rebase.patch
Patch2:           0002-Porting-optimized-longest_match.patch
Patch3:           0003-arm64-specific-build-patch.patch
Patch4:           0004-zlib-Optimize-CRC32.patch
Patch5:           zlib-1.2.11-SIMD.patch
Patch6:           0005-Accelerate-Adler32-using-arm64-SVE-instructions.patch
%endif

Patch6000:        fix-undefined-buffer-detected-by-oss-fuzz.patch

BuildRequires:    automake, autoconf, libtool

%description
Zlib is a free, general-purpose, not covered by any patents, lossless data-compression
library for use on virtually any computer hardware and operating system. The zlib data
format is itself portable across platforms.

%package          devel
Summary:          Header files and libraries for Zlib development
Requires:         %{name} = %{version}-%{release}

Provides:         zlib-static
Obsoletes:        zlib-static

%description      devel
This package contains the static library, the header files, the tests user case and other
development content.

%package          help
Summary:          Help documentation related to zlib
BuildArch:        noarch

%description      help
This package includes help documentation and manuals related to zlib.

%package          -n minizip
Summary:          Encapsulates the operations related to zip files
Requires:         %{name} = %{version}-%{release}

%description      -n minizip
Minizip is the upper library of zlib, which encapsulates the operations related to zip files.

%package          -n minizip-devel
Summary:          The development-related content related to minizip
Requires:         minizip = %{version}-%{release}
Requires:         %{name}-devel = %{version}-%{release}

%description      -n minizip-devel
This package contains the development-related content related to minizip.

%prep
%autosetup -p1

%build
export CFLAGS="$RPM_OPT_FLAGS"
%ifarch aarch64
CFLAGS+=" -DARM_NEON -O3"
CFLAGS+=" -march=armv8-a+crc"
%endif

./configure --libdir=%{_libdir} --includedir=%{_includedir} --prefix=%{_prefix}
%make_build LDFLAGS="$LDFLAGS -Wl,-z,relro -Wl,-z,now"

cd contrib/minizip
autoreconf --install
%configure --enable-static=no
%make_build

%install
%make_install

%make_install -C contrib/minizip
rm -f $RPM_BUILD_ROOT%_includedir/minizip/crypt.h

find $RPM_BUILD_ROOT -name '*.la' | xargs rm -f 

%check
make test

%files
%defattr(-,root,root)
%doc README ChangeLog FAQ
%{_libdir}/libz.so.*

%files devel
%doc doc/algorithm.txt test/example.c
%{_includedir}/zlib.h
%{_includedir}/zconf.h

%{_libdir}/libz.so
%{_libdir}/pkgconfig/zlib.pc
%{_libdir}/libz.a

%files help
%{_mandir}/man3/zlib.3*

%files -n minizip
%doc contrib/minizip/MiniZip64_info.txt contrib/minizip/MiniZip64_Changes.txt
%{_libdir}/libminizip.so.*


%files -n minizip-devel
%dir %{_includedir}/minizip
%{_includedir}/minizip/*.h

%{_libdir}/libminizip.so
%{_libdir}/pkgconfig/minizip.pc

%changelog
* Thu Apr 14 2022 YukariChiba <i@0x7f.cc> - 1.2.12-1
- Upgrade version to 1.2.12
- Merged patch in upstream: 5c44459 and 4346a16 for CVE-2018-25032

* Wed Apr 13 2022 tianwei <tianwei12@h-partners.com> - 1.2.11-20
- fix CVE-2018-25032

* Thu Sep 2 2021 liqiang <liqiang64@huawei.com> - 1.2.11-19
- Optimize Adler32 by SVE instructions.

* Mon Sep 14 2020 noah <hedongbo@huawei.com> - 1.2.11-18
- add zlib-1.2.11-SIMD.patch

* Sat Dec 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.2.11-17
- Fix undefined buffer detected by oss-fuzz

* Tue Dec 3 2019 liqiang <liqiang64@huawei.com> - 1.2.11-16
- Optimize CRC32 by NEON

* Thu Sep 5 2019 dongjian <dongjian13@huawei.com> - 1.2.11-15
- Rebuild the zlib and fix description
