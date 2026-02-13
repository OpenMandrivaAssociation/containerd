%bcond_with debug

%if %{with debug}
%global _dwz_low_mem_die_limit 0
%endif
%undefine _debugsource_packages

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

%global import_path github.com/containerd/containerd

#define beta 0

Name: containerd
Version:	2.2.1
Release:	%{?beta:0.%{beta}.}1
Summary: An industry-standard container runtime
License: ASL 2.0
URL: https://containerd.io
Source0: https://github.com/containerd/containerd/archive/v%{version}%{?beta:-%{beta}}/containerd-%{version}%{?beta:-%{beta}}.tar.gz
Source1: containerd.service
Source2: containerd.toml
BuildRequires:	make
BuildRequires: systemd-rpm-macros
%{?go_compiler:BuildRequires: compiler(go-compiler)}
BuildRequires: golang >= 1.10
BuildRequires: protobuf-compiler
BuildRequires: pkgconfig(protobuf) >= 3
BuildRequires: btrfs-devel
BuildRequires: go-md2man
BuildRequires: go-srpm-macros
%{?systemd_requires}
# https://github.com/containerd/containerd/issues/1508#issuecomment-335566293
Requires: (runc or crun)

%description
containerd is an industry-standard container runtime with an emphasis on
simplicity, robustness and portability. It is available as a daemon for Linux
and Windows, which can manage the complete container lifecycle of its host
system: image transfer and storage, container execution and supervision,
low-level storage and network attachments, etc.

%prep
%autosetup -n containerd-%{version}%{?beta:-%{beta}}

%build
%make_build PREFIX=%{_prefix}

%install
%make_install PREFIX=%{_prefix}

install -D -m 0644 %{S:1} %{buildroot}%{_unitdir}/containerd.service
install -D -m 0644 %{S:2} %{buildroot}%{_sysconfdir}/containerd/config.toml

ln -s containerd %{buildroot}%{_bindir}/docker-containerd
ln -s containerd-shim-runc-v2 %{buildroot}%{_bindir}/docker-containerd-shim

%files
%license LICENSE
%doc README.md
%{_bindir}/containerd
%{_bindir}/containerd-shim-runc-v2
%{_bindir}/containerd-stress
%{_bindir}/docker-containerd
%{_bindir}/docker-containerd-shim
%{_bindir}/ctr
%{_unitdir}/containerd.service
%dir %{_sysconfdir}/containerd
%config(noreplace) %{_sysconfdir}/containerd/config.toml
