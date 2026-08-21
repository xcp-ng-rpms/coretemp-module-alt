%define uname  %{kernel_version}
%define module_dir override

Summary: coretemp kernel module with a workaround for Xen restrictions
Name: coretemp-module-alt
Version: 1.0
Release: 5%{?dist}
# Built against new kABI after cip rebase
Requires: xcpng-kernel-kabi = 4.19.325-cip134+

License: GPL
#Source: https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/drivers/hwmon/coretemp.c?h=v4.19.19
Source: %{name}-%{version}.tar.gz

Patch0: coretemp-module-alt-1.0-disable-cpuid-check.patch

BuildRequires: kernel-devel
BuildRequires: gcc
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
With Xen patch https://xenbits.xen.org/gitweb/?p=xen.git;a=commitdiff;h=72e038450d3d5de1a39f0cfa2d2b0f9b3d43c6c6
Thermal and Performance information is now hidden from PV guests including Dom0.
This module skips check of CPU flag and reads MSR directly for Intel Package Thermal Status.

%prep
%autosetup -p1

%build
%{__make} -C /lib/modules/%{uname}/build M=$(pwd) modules

%install
%{__make} -C /lib/modules/%{uname}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# remove extra files modules_install copies in
rm -f %{buildroot}/lib/modules/%{uname}/modules.*

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{uname} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{uname}/*/*.ko

%changelog
* Fri Sep 16 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0-4
- Rebuild for XCP-ng 8.3

* Tue Jun 30 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0-3
- Rebuild for XCP-ng 8.2

* Thu Feb 13 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0-2
- Rebuild for XCP-ng 8.1

* Thu Dec 19 2019 Rushikesh Jadhav <rushikesh7@gmail.com> - 1.0-1
- Update spec file & version as per governance
- Renamed to coretemp-module-alt

* Wed Dec 4 2019 Rushikesh Jadhav <rushikesh7@gmail.com> - 1.0
- Added driver coretemp-module-1.0
- Removed cpuid checking from driver
