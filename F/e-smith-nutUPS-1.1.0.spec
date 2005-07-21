Summary: SME server - nut UPS interaction module
%define name e-smith-nutUPS
Name: %{name}
%define version 1.1.0
%define release 04
Version: %{version}
Release: %{release}
License: GPL
Vendor: Mitel Networks Corporation
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
Patch0: e-smith-nutUPS-1.1.0-02.mitel_patch
Patch1: e-smith-nutUPS-1.1.0-03.mitel_patch
Patch2: e-smith-nutUPS-1.1.0-04.mitel_patch
Packager: e-smith developers <bugs@e-smith.com>
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
Requires: nut nut-client daemontools
Requires: e-smith-lib >= 1.15.1-16
BuildArchitectures: noarch
BuildRequires: e-smith-devtools
AutoReqProv: no

%description
A module which configures the Network UPS Tools suite for operation with
the SME server software.

%changelog
* Tue Jul 12 2005 Charlie Brady <charlieb@e-smith.com>
- [1.1.0-04]
- Use generic_template_expand action in place of nutUPS-conf.
  [MN00064130]

* Tue Jul 12 2005 Charlie Brady <charlieb@e-smith.com>
- [1.1.0-03]
- Port to version 2.0 or nut (contributed by Shad Lords).
- Change nutups user to nut to confirm with new package
- Upgrade templates to support new 2.0 format [SF: 1226389]

* Thu Aug 21 2003 Charlie Brady <charlieb@e-smith.com>
- [1.1.0-02]
- Replace nutUPS-conf-startup action with default db fragments.
  [charlieb 9553]

* Thu Aug 21 2003 Charlie Brady <charlieb@e-smith.com>
- [1.1.0-01]
- Changing version to development stream number - 1.1.0

* Thu Jun 26 2003 Charlie Brady <charlieb@e-smith.com>
- [1.0.0-01]
- Creating stable version stream - 1.0.0

* Wed Jun  4 2003 Charlie Brady <charlieb@e-smith.com>
- [0.0.3-06]
- Create 'nutups' user via create-system-user. [charlieb 6033]

* Fri May  9 2003 Gordon Rowell <gordonr@e-smith.com>
- [0.0.3-05]
- Removed depedency on e-smith-email [gordonr 8405]

* Fri Apr 25 2003 Charlie Brady <charlieb@e-smith.com>
- [0.0.3-04]
- Change group and permissions of various configuration files, so that
  files can be reloaded by programs running non-root. This is a merge
  of Shad Lord's contributed code and my changes to use group read
  permission. [charlieb 8405]

* Fri Apr 25 2003 Tony Clayton <apc@e-smith.com>
- [0.0.3-03]
- Don't expand rc.modules template from nutUPS-conf [tonyc 2753]

* Fri Apr 25 2003 Charlie Brady <charlieb@e-smith.com>
- [0.0.3-02]
- Change group of nutUPS.notify script to nutups. [charlieb 8530]

* Wed Apr 16 2003 Tony Clayton <apc@e-smith.com>
- [0.0.3-01]
- Remove /etc/rc.modules altogether [tonyc 6556]

* Tue Mar 18 2003 Lijie Deng <lijied@e-smith.com>
- [0.0.2-12]
- Delete ./etc/rc.modules/template-begin,
  and modified %build [lijied 3295]

* Thu Jan 16 2003 Tony Clayton <apc@e-smith.com>
- [0.0.2-11]
- fix rc.modules usb drivers again [tonyc 2753]

* Mon Jan 13 2003 Tony Clayton <apc@e-smith.com>
- [0.0.2-10]
- fix rc.modules usb drivers to load conditionally [tonyc 2753]

* Mon Jan 13 2003 Tony Clayton <apc@e-smith.com>
- [0.0.2-09]
- send stdout/stderr to /dev/null when loading usb modules [tonyc 2753]

* Mon Jan 13 2003 Tony Clayton <apc@e-smith.com>
- [0.0.2-08]
- really adding usb* modules in rc.modules [tonyc 2753]

* Mon Jan 13 2003 Tony Clayton <apc@e-smith.com>
- [0.0.2-07]
- load usb* modules in rc.modules for hidups support
- add header to template-begin [tonyc 2753]

* Fri Jan 10 2003 Tony Clayton <apc@e-smith.com>
- [0.0.2-06]
- fix NOTIFYFLAG entries in upsmon.conf [tonyc 2753]
- turn off nut service by default [tonyc 2753]

* Thu Dec  5 2002 Charlie Brady <charlieb@e-smith.com>
- [0.0.2-05]
- Move mknod of device node to %post script. It can't run in %pre, because
  the enclosing directory has not yet been pulled out of the RPM archive.

* Thu Dec  5 2002 Charlie Brady <charlieb@e-smith.com>
- [0.0.2-04]
- Fix syntax errors in one of the upsmon.conf template fragments.
- Add ups runtime state directory. Create hiddev device node with
  appropriate permissions inside that directory.

* Wed Nov 27 2002 Charlie Brady <charlieb@e-smith.com>
- [0.0.2-03]
- Change configuration so that most UPS events are logged only to
  syslog, but SHUTDOWN is done using "signal-event". Response
  to UPS events can be tuned via config DB entries.

* Tue Nov 19 2002 Charlie Brady <charlieb@e-smith.com>
- [0.0.2-02]
- Add /etc/rc.d/init.d/nut symlink so that service starts up.
- Fix up a few broken templates.

* Mon Nov 18 2002 Charlie Brady <charlieb@e-smith.com>
- [0.0.2-01]
- Initial

%prep
%setup
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
perl createlinks

mkdir -p root/etc/rc.d/rc7.d
ln -s ../init.d/e-smith-service root/etc/rc.d/rc7.d/S15nut
mkdir -p root/etc/rc.d/init.d
ln -s ups root/etc/rc.d/init.d/nut

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-%{release}-filelist
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT \
    | sed -e '/nutUPS.notify/s/root,root/root,nut/' \
    > %{name}-%{version}-%{release}-filelist
echo '%dir %attr(750,nut,nut) /var/lib/ups' \
  >>  %{name}-%{version}-%{release}-filelist
echo '%ghost %attr(640,nut,nut) /var/lib/ups/hiddev0' \
  >>  %{name}-%{version}-%{release}-filelist
mkdir -p $RPM_BUILD_ROOT/var/lib/ups/
touch $RPM_BUILD_ROOT/var/lib/ups/hiddev0

%pre
/sbin/e-smith/create-system-user nut 57 'NUT UPS user' /var/lib/ups /bin/false

%post
if [ \! -e /var/lib/ups/hiddev0 ]
then
 mknod /var/lib/ups/hiddev0 c 180 96
 chown nut.nut  /var/lib/ups/hiddev0
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
