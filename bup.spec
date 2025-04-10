# disable tests on abf
# some tests need remote access
%bcond_with test

Name:		bup
Version:	0.33.7
Release:	1
Summary:	Efficient backup system based on the git packfile format
License:	LGPL-2.0-only
Group:		Archiving/Backup
URL:		https://bup.github.io/
Source0:	https://github.com/bup/bup/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:	python
BuildRequires:	pkgconfig(python3)
BuildRequires:	git
BuildRequires:	perl-Getopt-Long
BuildRequires:	perl-Pod-Usage
BuildRequires:	perl-Time-HiRes
BuildRequires:	python%{pyver}dist(fuse-python)
BuildRequires:	python%{pyver}dist(pylibacl)
BuildRequires:	python%{pyver}dist(pyxattr)
BuildRequires:	python%{pyver}dist(tornado)
%if %{with test}
BuildRequires:	python%{pyver}dist(pylint)
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(pytest-xdist)
BuildRequires:	parchive2
BuildRequires:	rsync
%endif
Requires:	git
Requires:	parchive2
Requires:	python%{pyver}dist(fuse-python)
Requires:	python%{pyver}dist(pylibacl)
Requires:	python%{pyver}dist(pyxattr)

%description
Bup is a very efficient backup system based on the git packfile format,
providing fast incremental saves and global deduplication (among and
within files, including virtual machine images).


%prep
%autosetup -n %{name}-%{version} -p1
# fix binpath
sed -i -e "s|PREFIX=/usr/local|PREFIX=%{_prefix}|g" GNUmakefile
# fix docpath
sed -i -e "s|/share/doc/bup|/share/doc/packages/bup|g" GNUmakefile
# fix env-script-interpreter
sed -i -e "s|\/usr\/bin\/env bash|\/bin\/bash|g" lib/cmd/bup-import-rdiff-backup
# rpmlint
find -type f -name ".gitignore" -exec rm {} \;

# NOTE removed problematic gc test
# NOTE check upstream if this test is fixed on next release
rm -f test/ext/test-gc-removes-incomplete-trees

%build
./configure
%make_build CFLAGS="%optflags"

%install
%make_install

%if %{with test}
%check
make check
%endif

%files
%{_bindir}/%{name}
%{_prefix}/lib/%{name}/%{name}
%{_prefix}/lib/%{name}/cmd
%{_prefix}/lib/%{name}/web
%doc README.md
%license LICENSE
