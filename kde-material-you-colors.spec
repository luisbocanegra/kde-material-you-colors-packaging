#
# spec file for package kde-material-you-colors
#
# Copyright (c) 2024 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#
%global kf6_version 6.0.0
%define qt6_version 6.6.0
%define kf5_version 5.102.0
%define qt5_version 5.15.2

# Full Plasma 6 version (e.g. 6.0.0)
%{!?_plasma6_bugfix: %define _plasma6_bugfix 6.0.0}
# Latest ABI-stable Plasma (e.g. 6.0 in KF6, but 6.0.80 in KUF)
%{!?_plasma6_version: %define _plasma6_version %(echo %{_plasma6_bugfix} | awk -F. '{print $1"."$2}')}
%define pythons python3
%{?!python_module:%define python_module() python-%{**} python3-%{**}}
%global debug_package %{nil}
Name:           kde-material-you-colors
Version:        1.9.1
Release:        1%{?dist}
Summary:        Automatic Material You Colors Generator from your wallpaper for the Plasma Desktop
License:        GNU General Public License v3 (GPLv3) (FIXME:No SPDX)
URL:            https://github.com/luisbocanegra/%{name}
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  cmake >= 3.16
%if 0%{?fedora}
BuildRequires:  extra-cmake-modules >= %{kf6_version}
BuildRequires:  libplasma-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  plasma5support-devel
BuildRequires:  python3-devel
Requires:       python3-dbus
Requires:       python3-pillow
Requires:       python-pywal
%else
BuildRequires:  kf6-extra-cmake-modules
BuildRequires:  libplasma6-devel
BuildRequires:  libQt5Gui-devel
BuildRequires:  libQt5DBus-devel
BuildRequires:  plasma5support6-devel
Requires:       python3-dbus-python
Requires:       libPlasma5Support6
Requires:       python311-Pillow
Requires:       %{python_module pywal >= 3.3.0}
%endif
BuildRequires:  python-rpm-macros
BuildRequires:  fdupes
BuildRequires:  %{python_module pip}
BuildRequires:  %{python_module setuptools >= 61.0}
# SECTION test requirements
BuildRequires:  %{python_module wheel >= 0.37.1}
BuildRequires:  %{python_module numpy >= 1.20}
Requires:       python-materialyoucolor >= 2.0.9
BuildArch:      x86_64

%description
Automatic Material You Colors Generator from your wallpaper for the Plasma Desktop

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%pyproject_wheel
cmake -B build -S . \
-DCMAKE_INSTALL_PREFIX=/usr \
-DINSTALL_PLASMOID=ON
cmake --build build

%install
%pyproject_install
DESTDIR="$RPM_BUILD_ROOT" cmake --install build

sed -i "1{/^#!\/usr\/bin\/env python3/d}" %{buildroot}%{python3_sitelib}/kde_material_you_colors/main.py
%fdupes %{buildroot}%{python3_sitelib}/%{name}/


%files
%doc README.md
%license LICENSE
%{_bindir}/kde-material-you-colors
%{python3_sitelib}/kde_material_you_colors/
%{python3_sitelib}/kde_material_you_colors-%{version}*.*-info/
%exclude %{python3_sitelib}/plasmoid/
%exclude %{python3_sitelib}/screenshot_helper
%{_bindir}/%{name}-screenshot-helper
/usr/share/applications/*
/usr/share/metainfo/*
/usr/share/plasma/plasmoids/*

%changelog
* Sun May 20 2024 Luis Bocanegra <luisbocanegra@users.noreply.github.com> 1.9.0-1
- new package built with tito
