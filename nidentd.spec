# TODO:
# - fix log file ownership (nobody must NOT own any files!)
Summary:	Simple identd
Summary(pl.UTF-8):	Prosty demon identa
Name:		nidentd
Version:	1.1
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://download.nmee.net/nidentd/%{name}-%{version}.tar.bz2
# Source0-md5:	e5bac34fb35269be48cb1bc07ac2bf96
Source1:	%{name}.inetd
Source2:	%{name}.logrotate
URL:		http://www.nmee.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	iptables
Provides:	identserver
Obsoletes:	linux-identd
Obsoletes:	linux-identd-inetd
Obsoletes:	linux-identd-standalone
Obsoletes:	pidentd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A simple identd written in Perl, with support for masqueraded
connections (using iptables). It does a reverse lookup on the
masqueraded host, and uses the first part of the hostname as the ident
reply. If the ip address can't be resolved, it uses the ident reply as
specified by the $default variable in the program (e.g. if the local
host on the lan is 192.168.0.100, and that address resolves to
pc1.local.lan in a reverse lookup, the ident reply will be 'pc1').

%description -l pl.UTF-8
Prosty demon identd napisany w Perlu z obsługą dla maskowanych
połączeń (używa iptables). Rozwiązuje nazwę na maskującym hoście i
używa jako identa pierwszego członu nazwy hosta. Jeśli adres ip nie
może być rozwiązany, to używa zmiennej $default zawartej w programie
(na przykład jeśli adres 192.168.0.100 jest rozwiązywany jako
pc1.local.lan, to identd przydzieli identa 'pc1').

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/sysconfig/rc-inetd,%{_sysconfdir}/logrotate.d,%{_sbindir},%{_var}/log}

install nidentd $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/nidentd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/nidentd

:> $RPM_BUILD_ROOT/var/log/nidentd.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q rc-inetd reload

%postun
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/nidentd
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/nidentd
%attr(600,nobody,root) %ghost %{_var}/log/nidentd.log # FIXME nobody user/group can't own files! -adapter.awk
