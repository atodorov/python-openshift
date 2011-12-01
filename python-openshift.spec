# Copyright 2011 Alexander Todorov <atodorov@nospam.otb.bg>

%define pkgname %(%{__python} setup.py --name)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary:	%(%{__python} setup.py --description)
Name:		python-%{pkgname}
Version:	%(%{__python} setup.py --version)
Release:	1%{?dist}
License:	%(%{__python} setup.py --license)
Group:		Development/Languages
URL:		%(%{__python} setup.py --url)
Source:		%{url}/%{pkgname}-%{version}.tar.gz
BuildRequires:	python-devel, python-setuptools
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This is a Python interface to Red Hat's OpenShift cloud platform
based on the OpenShift API docs.

%prep
%setup -q -c -n %{pkgname}

%build
%{__python} setup.py build

pydoc -w openshift


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

mkdir -p %{buildroot}/%{_docdir}/%{name}-%{version}
install -m 0644 README %{buildroot}/%{_docdir}/%{name}-%{version}
install -m 0644 LICENSE %{buildroot}/%{_docdir}/%{name}-%{version}
install -m 0644 openshift.html %{buildroot}/%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%defattr(-,root,root)

%{python_sitelib}/%{pkgname}/
%if 0%{?el6}
%{python_sitelib}/%{pkgname}-%{version}-*.egg-info
%endif

%doc README
%doc LICENSE
%doc *.html

%changelog

* Sun Nov 27 2011 Alexander Todorov <atodorov@nospam.otb.bg> 0.1-1
- Initial spec file for Fedora and Red Hat Enterprise Linux
