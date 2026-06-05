# Do not check any files in docdir for requires
%global __requires_exclude_from ^%{_docdir}/.*$

%define devname %mklibname rtl_433 -d

# html doc/api building
%bcond docs 1

Name:		rtl_433
Version:	25.12
Release:	2
Summary:	Program to decode radio transmissions from devices on the ISM bands (and other frequencies)
URL:		https://github.com/merbanan/rtl_433
License:	GPL-2.0-only
Group:		Communications/Radio
Source0:	https://github.com/merbanan/rtl_433/archive/%{version}/%{name}-%{version}.tar.gz
# Make doxygen use svg image format & enable svg interactivity
Patch0:		rtl_433-25.12-doxygen-fixes.patch

BuildRequires:	cmake
BuildRequires:	ninja
%if %{with docs}
BuildRequires:	doxygen
BuildRequires:	fdupes
BuildRequires:	graphviz
%endif
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(librtlsdr)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(SoapySDR)
%if %{with docs}
Recommends:	%{name}-doc
%endif

%description
rtl_433 (despite the name) is a generic data receiver, mainly for the
433.92 MHz, 868 MHz (SRD), 315 MHz, 345 MHz, and 915 MHz ISM bands.

It works with RTL-SDR and/or SoapySDR. Actively tested and supported
are Realtek RTL2832 based DVB dongles (using RTL-SDR) and LimeSDR
(LimeSDR USB and LimeSDR mini engineering samples kindly provided by
MyriadRf), PlutoSDR, HackRF One (using SoapySDR drivers), as well
as SoapyRemote.

For documentation install the %{name}-docs package or see https://triq.org/rtl_433/

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name} = %{EVRD}
%if %{with docs}
Recommends:	%{name}-doc = %{version}-%{release}
%endif

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%if %{with docs}
%package doc
Summary:	Documentation files for %{name} and %{devname}
Group:		Development/C
BuildArch:	noarch

%description doc
Documentation files for %{name} and %{devname}.

Contains user documentation, example scripts and the developer/api
documentation in the doc/%{name}-doc/html folder.
%endif

%prep
%autosetup -n %{name}-%{version} -p1
# remove git dir
rm -rf .git/
%if %{with docs}
# tweak doxyfile
sed -i -e 's/SHOW_USED_FILES        = YES/SHOW_USED_FILES        = NO/g' Doxyfile.in
sed -i -e 's/HTML_TIMESTAMP         = YES/HTML_TIMESTAMP         = NO/g' Doxyfile.in
sed -i -e 's/DOT_IMAGE_FORMAT       = png/DOT_IMAGE_FORMAT       = svg/g' Doxyfile.in
sed -i -e 's/INTERACTIVE_SVG        = NO/INTERACTIVE_SVG        = YES/g' Doxyfile.in
%endif

%build
%cmake \
	-DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
%if %{with docs}
	-DBUILD_DOCUMENTATION=ON \
%endif
	-G Ninja

%ninja_build

%install
%ninja_install -C build

# install example config file as main config file
install -Dm 644 %{buildroot}%{_sysconfdir}/%{name}/rtl_433.example.conf %{buildroot}%{_sysconfdir}/%{name}/rtl_433.conf
%if %{with docs}
# install html docs
cd build/doc/
find html/ -type f -exec install -Dpm 644 "{}" "%{buildroot}%{_docdir}/%{name}-doc/{}" \;
cd ../../
%fdupes %{buildroot}%{_docdir}/%{name}-doc/html/
%endif

%files
%doc README.md
%license COPYING
%{_bindir}/rtl_433
%{_mandir}/*/%{name}.1*
%config(noreplace) %{_sysconfdir}/%{name}/*.conf

%if %{with docs}
%files doc
%doc README.md
%license COPYING
%doc docs/*.md
%doc examples
%doc %{_docdir}/%{name}-doc/html
%endif

%files -n %{devname}
%license COPYING
%{_includedir}/rtl_433*.h
