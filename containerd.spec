%bcond_without ctr
%bcond_with debug

%if %{with debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};

%global import_path github.com/containerd/containerd

Name: containerd
Version: 1.0.2
%global commit 9b55aab90508bd389d7654c4baf173a981477d55
%global tag v%{version}
Release: 1%{?dist}
Summary: An industry-standard container runtime
License: ASL 2.0
URL: https://containerd.io
Source0: https://%{import_path}/archive/%{tag}/containerd-%{version}.tar.gz
Source1: containerd.service
Source2: containerd.toml
%{?go_compiler:BuildRequires: compiler(go-compiler)}
BuildRequires: golang >= 1.8
BuildRequires: systemd
BuildRequires: btrfs-devel
%{?systemd_requires}
# https://github.com/containerd/containerd/issues/1508#issuecomment-335566293
Requires: runc >= 1.0.0
# vendored libraries
# awk '{print "Provides: bundled(golang("$1")) = "$2}' containerd-*/vendor.conf | sort
Provides: bundled(golang(github.com/beorn7/perks)) = 4c0e84591b9aa9e6dcfdf3e020114cd81f89d5f9
Provides: bundled(golang(github.com/boltdb/bolt)) = e9cf4fae01b5a8ff89d0ec6b32f0d9c9f79aefdd
Provides: bundled(golang(github.com/BurntSushi/toml)) = 99064174e013895bbd9b025c31100bd1d9b590ca
Provides: bundled(golang(github.com/containerd/btrfs)) = cc52c4dea2ce11a44e6639e561bb5c2af9ada9e3
Provides: bundled(golang(github.com/containerd/cgroups)) = 29da22c6171a4316169f9205ab6c49f59b5b852f
Provides: bundled(golang(github.com/containerd/console)) = 84eeaae905fa414d03e07bcd6c8d3f19e7cf180e
Provides: bundled(golang(github.com/containerd/continuity)) = cf279e6ac893682272b4479d4c67fd3abf878b4e
Provides: bundled(golang(github.com/containerd/fifo)) = fbfb6a11ec671efbe94ad1c12c2e98773f19e1e6
Provides: bundled(golang(github.com/containerd/go-runc)) = ed1cbe1fc31f5fb2359d3a54b6330d1a097858b7
Provides: bundled(golang(github.com/containerd/typeurl)) = f6943554a7e7e88b3c14aad190bf05932da84788
Provides: bundled(golang(github.com/coreos/go-systemd)) = 48702e0da86bd25e76cfef347e2adeb434a0d0a6
Provides: bundled(golang(github.com/davecgh/go-spew)) = v1.1.0
Provides: bundled(golang(github.com/dmcgowan/go-tar)) = go1.10
Provides: bundled(golang(github.com/docker/go-events)) = 9461782956ad83b30282bf90e31fa6a70c255ba9
Provides: bundled(golang(github.com/docker/go-metrics)) = 8fd5772bf1584597834c6f7961a530f06cbfbb87
Provides: bundled(golang(github.com/docker/go-units)) = v0.3.1
Provides: bundled(golang(github.com/godbus/dbus)) = c7fdd8b5cd55e87b4e1f4e372cdb1db61dd6c66f
Provides: bundled(golang(github.com/gogo/protobuf)) = v0.5
Provides: bundled(golang(github.com/golang/protobuf)) = 1643683e1b54a9e88ad26d98f81400c8c9d9f4f9
Provides: bundled(golang(github.com/grpc-ecosystem/go-grpc-prometheus)) = 6b7015e65d366bf3f19b2b2a000a831940f0f7e0
Provides: bundled(golang(github.com/matttproud/golang_protobuf_extensions)) = v1.0.0
Provides: bundled(golang(github.com/Microsoft/go-winio)) = v0.4.4
Provides: bundled(golang(github.com/Microsoft/hcsshim)) = v0.6.7
Provides: bundled(golang(github.com/Microsoft/opengcs)) = v0.3.2
Provides: bundled(golang(github.com/opencontainers/go-digest)) = 21dfd564fd89c944783d00d069f33e3e7123c448
Provides: bundled(golang(github.com/opencontainers/image-spec)) = v1.0.0
Provides: bundled(golang(github.com/opencontainers/runc)) = 7f24b40cc5423969b4554ef04ba0b00e2b4ba010
Provides: bundled(golang(github.com/opencontainers/runtime-spec)) = v1.0.0
Provides: bundled(golang(github.com/pkg/errors)) = v0.8.0
Provides: bundled(golang(github.com/pmezard/go-difflib)) = v1.0.0
Provides: bundled(golang(github.com/prometheus/client_golang)) = v0.8.0
Provides: bundled(golang(github.com/prometheus/client_model)) = fa8ad6fec33561be4280a8f0514318c79d7f6cb6
Provides: bundled(golang(github.com/prometheus/common)) = 195bde7883f7c39ea62b0d92ab7359b5327065cb
Provides: bundled(golang(github.com/prometheus/procfs)) = fcdb11ccb4389efb1b210b7ffb623ab71c5fdd60
Provides: bundled(golang(github.com/sirupsen/logrus)) = v1.0.0
Provides: bundled(golang(github.com/stevvooe/ttrpc)) = d2710463e497617f16f26d1e715a3308609e7982
Provides: bundled(golang(github.com/stretchr/testify)) = v1.1.4
Provides: bundled(golang(github.com/urfave/cli)) = 7bc6a0acffa589f415f88aca16cc1de5ffd66f9c
Provides: bundled(golang(golang.org/x/net)) = 7dcfb8076726a3fdd9353b6b8a1f1b6be6811bd6
Provides: bundled(golang(golang.org/x/sync)) = 450f422ab23cf9881c94e2db30cac0eb1b7cf80c
Provides: bundled(golang(golang.org/x/sys)) = 314a259e304ff91bd6985da2a7149bbf91237993
Provides: bundled(golang(golang.org/x/text)) = 19e51611da83d6be54ddafce4a4af510cb3e9ea4
Provides: bundled(golang(google.golang.org/genproto)) = d80a6e20e776b0b17a324d0ba1ab50a39c8e8944
Provides: bundled(golang(google.golang.org/grpc)) = v1.7.2


%description
containerd is an industry-standard container runtime with an emphasis on
simplicity, robustness and portability. It is available as a daemon for Linux
and Windows, which can manage the complete container lifecycle of its host
system: image transfer and storage, container execution and supervision,
low-level storage and network attachments, etc.


%prep
%setup -qn containerd-%{version}

%build
export CC=gcc
export CXX=g++
mkdir -p src/%(dirname %{import_path})
ln -s ../../.. src/%{import_path}
export GOPATH=$(pwd):%{gopath}
export LDFLAGS="-X %{import_path}/version.Package=%{import_path} -X %{import_path}/version.Version=%{tag} -X %{import_path}/version.Revision=%{commit}"
%gobuild -o bin/containerd %{import_path}/cmd/containerd
%gobuild -o bin/containerd-shim %{import_path}/cmd/containerd-shim
%{?with_ctr:%gobuild -o bin/ctr %{import_path}/cmd/ctr}

%install
install -D -m 0755 bin/containerd %{buildroot}%{_bindir}/containerd
install -D -m 0755 bin/containerd-shim %{buildroot}%{_bindir}/containerd-shim
%{?with_ctr:install -D -m 0755 bin/ctr %{buildroot}%{_bindir}/ctr}
install -D -m 0644 %{S:1} %{buildroot}%{_unitdir}/containerd.service
install -D -m 0644 %{S:2} %{buildroot}%{_sysconfdir}/containerd/config.toml
ln -s containerd %{buildroot}%{_bindir}/docker-containerd
ln -s containerd-shim %{buildroot}%{_bindir}/docker-containerd-shim

%post
%systemd_post containerd.service

%preun
%systemd_preun containerd.service

%postun
%systemd_postun_with_restart containerd.service

%files
%{_bindir}/containerd
%{_bindir}/docker-containerd
%{_bindir}/docker-containerd-shim
%{_bindir}/containerd-shim
%{?with_ctr:%{_bindir}/ctr}
%{_unitdir}/containerd.service
%config(noreplace) %{_sysconfdir}/containerd/config.toml
