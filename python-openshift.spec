# Copyright 2011 Alexander Todorov <atodorov@nospam.otb.bg>

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary:	Python interface to Red Hat's OpenShift cloud platform
Name:		python-openshift
Version:	0.1
Release:	1%{?dist}
License:	MIT
Group:		Development/Languages
URL:		https://github.com/atodorov/python-openshift
Source:		%{pkgname}-%{version}.tar.gz
BuildRequires:	python-devel, python-setuptools
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This is a Python interface to Red Hat's OpenShift cloud platform
based on the OpenShift API docs.

%prep
%setup -q -n %{pkgname}-%{version}

%build
%{__python} setup.py build

pydoc -w openshift


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

mkdir -p %{buildroot}/%{_docdir}/%{name}-%{version}
install -m 0644 README %{buildroot}/%{_docdir}/%{name}-%{version}
install -m 0644 LICENCE %{buildroot}/%{_docdir}/%{name}-%{version}
install -m 0644 openshift.html %{buildroot}/%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%defattr(-,root,root)

%{python_sitelib}/openshift/
%if 0%{?el6}
%{python_sitelib}/python_openshift-%{version}-*.egg-info
%endif

%doc README
%doc LICENCE
%doc *.html

%changelog

* Sun Nov 27 2011 Alexander Todorov <atodorov@nospam.otb.bg> 0.1-1
- Initial spec file for Fedora and Red Hat Enterprise Linux
