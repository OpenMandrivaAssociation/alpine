Summary: Command line email client
Name: alpine
Version: 2.26
Release: 2
License: Apache License
Group: Networking/Mail
Source: https://alpineapp.email/alpine/release/src/alpine-%{version}.tar.xz
Patch0: https://alpineapp.email/alpine/patches/alpine-%{version}/all.patch.gz
Patch1: alpine-2.00-link.patch
Patch2: alpine-2.26-no-Lusrlib.patch
URL: http://alpineapp.email/
BuildRequires: aspell
BuildRequires: pkgconfig(ncurses)
BuildRequires: pam-devel
BuildRequires: pkgconfig(openssl)
BuildRequires: openldap-devel
BuildRequires: gettext-devel
Conflicts: pine
Requires: aspell
Requires: mailcap

%description
Alpine is a tool for reading, sending, and managing e-mail and 
internet news (usenet) messages. It is the successor to Pine and 
was developed by Computing & Communications at the University of
Washington.

Though originally designed for inexperienced email users,
Alpine supports many advanced features and a large number of
configuration and personal-preference options.

This package contains re-alpine, a continuation of alpine. It is
patched to add support for maildir style mailboxes.

%prep
%autosetup -p1 -n %{name}-%{version}
touch imap/ip6
%configure --without-krb5 \
           --without-tcl \
           --with-c-client-target=lfd \
           --with-passfile=.alpine.passfile \
           --with-system-pinerc=%{_sysconfdir}/pine.conf \
           --with-system-fixed-pinerc=%{_sysconfdir}/pine.conf.fixed

%build
%make_build

%install
%make_install

# create/touch %ghost'd files
mkdir -p %{buildroot}%{_sysconfdir}
touch %{buildroot}%{_sysconfdir}/pine.conf
touch %{buildroot}%{_sysconfdir}/pine.conf.fixed

%files
%doc README LICENSE
%{_bindir}/alpine
%{_bindir}/pico
%{_bindir}/pilot
%{_bindir}/rpload
%{_bindir}/rpdump
%{_mandir}/man1/alpine.1*
%{_mandir}/man1/pico.1*
%{_mandir}/man1/pilot.1*
%{_mandir}/man1/rpload.1*
%{_mandir}/man1/rpdump.1*
%ghost %config(noreplace) %{_sysconfdir}/pine.conf
%ghost %config(noreplace) %{_sysconfdir}/pine.conf.fixed
