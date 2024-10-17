%define module_name lenovo-sl-laptop
%define module_path %{_usrsrc}/%{module_name}-%{version}-%{release}

Summary:	Lenovo ThinkPad SL Series Exerimental Driver
Name:		dkms-%{module_name}
Version:	0.02
Release:	3
License:	GPLv2+
URL:		https://github.com/tetromino/lenovo-sl-laptop/tree/master
Group:		System/Kernel and hardware
Source0:	%{module_name}.tar.bz2
Patch0:		lenovo-sl-laptop-dmi.patch
BuildArch:	noarch
Requires(pre):	dkms
Requires(post):	dkms

%description
This is an experimental driver for the Lenovo ThinkPad SL
series, since those laptops are currently not supported by
the thinkpad_acpi driver.

%prep
%setup -q -n %{module_name}
%patch0 -p0

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{module_path}
cp -a * %{buildroot}/%{module_path}
cat > %{buildroot}/%{module_path}/dkms.conf <<EOF
PACKAGE_VERSION="%{version}-%{release}"
# Items below here should not have to change with each driver version
PACKAGE_NAME="%{module_name}"
DEST_MODULE_LOCATION[0]="/kernel/3rdparty/%{module_name}"
BUILT_MODULE_NAME[0]="%{module_name}"
REMAKE_INITRD="no"
AUTOINSTALL="yes"
EOF
mkdir -p %{buildroot}/etc/modprobe.d/
cat > %{buildroot}/etc/modprobe.d/%name <<EOF
options %{module_name} control_backlight=1
blacklist video
EOF

%clean
rm -rf %{buildroot}

%post
dkms add     -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade
dkms build   -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade
dkms install -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade

%preun
dkms remove  -m %{module_name} -v %{version}-%{release} --all --rpm_safe_upgrade

%files
%defattr(-,root,root)
%{module_path}
/etc/modprobe.d/dkms-lenovo-sl-laptop



%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0.02-0.2mdv2011.0
+ Revision: 617790
- the mass rebuild of 2010.0 packages

* Wed Jun 10 2009 Pascal Terjan <pterjan@mandriva.org> 0.02-0.1mdv2010.0
+ Revision: 384767
- import dkms-lenovo-sl-laptop


* Wed Jun 10 2009 Pascal Terjan <pterjan@mandriva.org> 0.02-0.1mdv2010.0
- first package
