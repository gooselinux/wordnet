Name:           wordnet
Version:        3.0
Release:        13%{?dist}
Summary:        A lexical database for the English language

Group:          Applications/Text
License:        MIT and GPLv2+
URL:            http://wordnet.princeton.edu
Source0:        http://wordnetcode.princeton.edu/%{version}/WordNet-%{version}.tar.bz2
Patch0:         wordnet-3.0-CVE-2008-2149.patch
Patch1:         wordnet-3.0-CVE-2008-3908.patch
Patch2:         wordnet-3.0-fix_man.patch
Patch3:         wordnet-3.0-fix_resourcedir_path.patch
Patch4:         wordnet-3.0-src_stubs_c.patch
# wordnet-3.0-wishwn_manpage.patch is GPLv2+
Patch5:         wordnet-3.0-wishwn_manpage.patch
Patch6:         wordnet-3.0-use_system_tk_headers.patch
Patch7:         wordnet-3.0-libtool.patch
# Bug #585199
Patch8:         wordnet-3.0-error_message.patch
Requires:       tcl, tk
BuildRequires:  automake >= 1.8
BuildRequires:  libtool
BuildRequires:  tcl-devel
BuildRequires:  tk-devel
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
WordNet is a large lexical database of English, developed under the direction
of George A. Miller. Nouns, verbs, adjectives and adverbs are grouped into sets
of cognitive synonyms (synsets), each expressing a distinct concept. Synsets
are interlinked by means of conceptual-semantic and lexical relations. The
resulting network of meaningfully related words and concepts can be navigated
with the browser. WordNet is also freely and publicly available for download.
WordNet's structure makes it a useful tool for computational linguistics and
natural language processing.

%package devel
Summary:    The development libraries and header files for WordNet
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   tcl-devel, tk-devel

%description devel
This package contains the libraries and header files required to create
applications based on WordNet.

%prep
%setup -q -n WordNet-3.0
%patch0 -p1 -b .cve-2008-2149
%patch1 -p1 -b .cve-2008-3908
%patch2 -p1 -b .fix_man
%patch3 -p1 -b .fix_resourcedir_path
%patch4 -p1 -b .src_stubs_c
%patch5 -p1 -b .wishwn_manpage
sed -e '/man_MANS/ s/$/ wishwn.1/' -i doc/man/Makefile.am
%patch6 -p1 -b .use_system_tk_headers
%patch7 -p1 -b .libtool
%patch8 -p1 -b .error_message
# delete the include/tk dir, since we do not use the included tk headers
rm -rf include/tk


%build
libtoolize && aclocal
autoupdate
autoreconf -i
%configure --enable-static=no --prefix=%{_datadir}/wordnet-%{version}/
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# delete the libWN.la files (reasoning in the packaging guidelines)
rm -f  $RPM_BUILD_ROOT%{_libdir}/libWN.la
# Remove duplicate copies of docs installed by make install
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/doc


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL ChangeLog README doc/{html,ps,pdf}
%{_bindir}/wishwn
%{_bindir}/wn
%{_bindir}/wnb
%{_mandir}/man1/*.1.gz
%{_mandir}/man5/*.5.gz
%{_mandir}/man7/*.7.gz
%{_datadir}/%{name}-%{version}/
%{_libdir}/libWN.so.*

%files devel
%defattr(-,root,root,-)
%{_mandir}/man3/*.3.gz
%{_includedir}/wn.h
%{_libdir}/libWN.so


%changelog
* Fri Apr 30 2010 Petr Pisar <ppisar@redhat.com> - 3.0-13
- Add GPLv2+ license tag because wishwn(1) manual page is GPLv2+-licensed.

* Wed Apr 28 2010 Petr Pisar <ppisar@redhat.com> - 3.0-12
- Install wishwn(1) manual page
- Remove libX11-devel and libXft-devel BuildRequires as they are inherited
  from tk-devel. Keep tcl-devel as tcl.h is included directly.
- Devel subpackage requires tcl-devel and tk-devel.

* Thu Apr 23 2010 Petr Pisar <ppisar@redhat.com> - 3.0-11
- Fix error message printing (#585199)
- Fix Source0 URL and Summary typo

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 3.0-10.1
- Rebuilt for RHEL 6

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Caolan McNamara <caolanm@redhat.com> - 3.0-9
- Fixed fedora BZ 504957 - references to non-existing dirs in wnb

* Wed May 27 2009 Steven Fernandez <steve@lonetwin.net> - 3.0-8
- Fixed issues with the doc files duplication and ownership

* Wed May 27 2009 Steven Fernandez <steve@lonetwin.net> - 3.0-7
- Modified the %%files sections for both packages to only include the link in
  the devel package and the .so in the main package.
- Added %%pre and %%post sections

* Wed May 27 2009 Steven Fernandez <steve@lonetwin.net> - 3.0-6
- Added commands to build only shared libs and remove libtool's .la files
  before packaging

* Tue May 19 2009 Steven Fernandez <steve@lonetwin.net> - 3.0-5
- Added the libtool patch to build libWN.so dynamic lib

* Wed Feb 18 2009 Steven Fernandez <steve@lonetwin.net> - 3.0-4
- Added Tom 'spot' Callaway's patch to not include the tk.h and tkDecls.h from
  the upstream source, but instead rely on system tk headers

* Sun Jan 18 2009 Steven Fernandez <steve@lonetwin.net> - 3.0-3
- renamed rpm from WordNet to wordnet to be more consistent with other distos
- split the devel package
- borrowed more patches from the debian package

* Tue Jan 13 2009 Steven Fernandez <steve@lonetwin.net> - 3.0-2
- patch to fix CVE-2008-3908
- Added the wishwn man page from the debian wordnet package

* Sat Nov 29 2008 Steven Fernandez <steve@lonetwin.net> - 3.0-1
- First build for Fedora 10

