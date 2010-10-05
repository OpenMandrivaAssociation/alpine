Summary: University of Washington Pine mail user agent
Name: alpine
Version: 2.00
Release: %mkrel 6
License: Apache License
Group: Networking/Mail
Source: ftp://ftp.cac.washington.edu/alpine/%{name}-%{version}.tar.bz2
Patch0: alpine-2.00-string-format.patch
Patch1: alpine-2.00-link.patch
URL: http://www.washington.edu/alpine
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: aspell
BuildRequires: ncurses-devel
BuildRequires: pam-devel
BuildRequires: libopenssl-devel
BuildRequires: libldap-devel
BuildRequires: gettext-devel
Conflicts: pine
Requires: aspell
Requires: mailcap

%description
Alpine -- an Alternatively Licensed Program for Internet
News & Email -- is a tool for reading, sending, and managing
electronic messages.  Alpine is the successor to Pine and was
developed by Computing & Communications at the University of
Washington.  
Though originally designed for inexperienced email users,
Alpine supports many advanced features, and an ever-growing number of
configuration and personal-preference options.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .stft
%patch1 -p0 -b .link

%build
autoreconf -fi
touch imap/ip6
%configure2_5x --without-krb5 \
           --without-tcl \
           --with-c-client-target=lfd \
           --with-spellcheck-prog=aspell \
           --with-passfile=.alpine.passfile \
           --with-system-pinerc=%{_sysconfdir}/pine.conf \
           --with-system-fixed-pinerc=%{_sysconfdir}/pine.conf.fixed


%make

%install
rm -rf %{buildroot}
%makeinstall_std

install -D -m755 imap/mailutil/mailutil $RPM_BUILD_ROOT%{_bindir}/mailutil
if ! install -D -m2755 -gmail imap/mlock/mlock $RPM_BUILD_ROOT%{_sbindir}/mlock; then
install -D -m755 imap/mlock/mlock $RPM_BUILD_ROOT%{_sbindir}/mlock
echo "*** DO NOT FORGET TO DO THE FOLLOWING BY HAND while root:
***  chgrp mail $RPM_BUILD_ROOT%{_sysconfdir}/mlock
***  echo chmod 2755 $RPM_BUILD_ROOT%{_sysconfdir}/mlock"
fi
install -D -m644 imap/src/mailutil/mailutil.1 $RPM_BUILD_ROOT%{_mandir}/man1/mailutil.1

# create/touch %ghost'd files
mkdir -p %{buildroot}%{_sysconfdir}
touch %{buildroot}%{_sysconfdir}/pine.conf
touch %{buildroot}%{_sysconfdir}/pine.conf.fixed

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README LICENSE doc/tech-notes.txt
%{_bindir}/alpine
%{_bindir}/pico
%{_bindir}/pilot
%{_bindir}/rpload
%{_bindir}/rpdump
%{_bindir}/mailutil
%attr(2755, root, mail) %{_sbindir}/mlock
%{_mandir}/man1/alpine.1*
%{_mandir}/man1/pico.1*
%{_mandir}/man1/pilot.1*
%{_mandir}/man1/rpload.1*
%{_mandir}/man1/rpdump.1*
%{_mandir}/man1/mailutil.1*
%ghost %config(noreplace) %{_sysconfdir}/pine.conf
%ghost %config(noreplace) %{_sysconfdir}/pine.conf.fixed

