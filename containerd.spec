%bcond_with debug

%if %{with debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

%global import_path github.com/containerd/containerd

Name: containerd
Version: 1.2.2
%global commit 9754871865f7fe2f4e74d43e2fc7ccd237edcbce
%global tag v%{version}
Release: 2
Epoch:	1
Summary: An industry-standard container runtime
License: ASL 2.0
URL: https://containerd.io
Source0: https://%{import_path}/archive/%{tag}/containerd-%{version}.tar.gz
Source1: containerd.service
Source2: containerd.toml
ExclusiveArch: %{go_arches}
BuildRequires: systemd
%{?go_compiler:BuildRequires: compiler(go-compiler)}
BuildRequires: golang >= 1.10
BuildRequires: protobuf-compiler
BuildRequires: pkgconfig(protobuf) >= 3
BuildRequires: btrfs-devel
BuildRequires: go-md2man
%{?systemd_requires}
# https://github.com/containerd/containerd/issues/1508#issuecomment-335566293
Requires: runc >= 1.0.0
# vendored libraries
# grep -v -e '^$' -e '^#' containerd-*/vendor.conf | awk '{print "Provides: bundled(golang("$1")) = "$2}' | sort
Provides: bundled(golang(github.com/containerd/aufs)) = ffa39970e26ad01d81f540b21e65f9c1841a5f92
Provides: bundled(golang(github.com/containerd/cgroups)) = 5e610833b72089b37d0e615de9a92dfc043757c2
Provides: bundled(golang(github.com/containerd/console)) = c12b1e7919c14469339a5d38f2f8ed9b64a9de23
Provides: bundled(golang(github.com/containerd/continuity)) = bd77b46c8352f74eb12c85bdc01f4b90f69d66b4
Provides: bundled(golang(github.com/containerd/cri)) = f913714917d2456d7e65a0be84962b1ce8acb487
Provides: bundled(golang(github.com/containerd/go-cni)) = 40bcf8ec8acd7372be1d77031d585d5d8e561c90
Provides: bundled(golang(github.com/containerd/go-runc)) = 5a6d9f37cfa36b15efba46dc7ea349fa9b7143c3
Provides: bundled(golang(github.com/containerd/ttrpc)) = 2a805f71863501300ae1976d29f0454ae003e85a
Provides: bundled(golang(github.com/containerd/typeurl)) = a93fcdb778cd272c6e9b3028b2f42d813e785d40
Provides: bundled(golang(github.com/emicklei/go-restful)) = 2.2.1
Provides: bundled(golang(github.com/ghodss/yaml)) = 1.0.0
Provides: bundled(golang(github.com/golang/protobuf)) = 1.1.0
Provides: bundled(golang(github.com/json-iterator/go)) = 1.1.5
Provides: bundled(golang(github.com/Microsoft/go-winio)) = 0.4.11
Provides: bundled(golang(github.com/Microsoft/hcsshim)) = 0.7.12
Provides: bundled(golang(github.com/modern-go/concurrent)) = 1.0.3
Provides: bundled(golang(github.com/modern-go/reflect2)) = 1.0.1
Provides: bundled(golang(github.com/opencontainers/go-digest)) = c9281466c8b2f606084ac71339773efd177436e7
Provides: bundled(golang(github.com/opencontainers/runc)) = 58592df56734acf62e574865fe40b9e53e967910
Provides: bundled(golang(github.com/opencontainers/runtime-spec)) = eba862dc2470385a233c7507392675cbeadf7353
Provides: bundled(golang(github.com/opencontainers/runtime-tools)) = 0.6.0
Provides: bundled(golang(github.com/opencontainers/selinux)) = b6fa367ed7f534f9ba25391cc2d467085dbb445a
Provides: bundled(golang(github.com/tchap/go-patricia)) = 2.2.6
Provides: bundled(golang(github.com/xeipuuv/gojsonpointer)) = 4e3ac2762d5f479393488629ee9370b50873b3a6
Provides: bundled(golang(github.com/xeipuuv/gojsonreference)) = bd5ef7bd5415a7ac448318e64f11a24cd21e594b
Provides: bundled(golang(github.com/xeipuuv/gojsonschema)) = 1d523034197ff1f222f6429836dd36a2457a1874
Provides: bundled(golang(go.etcd.io/bbolt)) = 1.3.1-etcd.8
Provides: bundled(golang(golang.org/x/net)) = b3756b4b77d7b13260a0a2ec658753cf48922eac
Provides: bundled(golang(golang.org/x/oauth2)) = a6bd8cefa1811bd24b86f8902872e4e8225f74c4
Provides: bundled(golang(golang.org/x/sys)) = 1b2967e3c290b7c545b3db0deeda16e9be4f98a2
Provides: bundled(golang(google.golang.org/grpc)) = 1.12.0
Provides: bundled(golang(gopkg.in/yaml.v2)) = 2.2.1
Provides: bundled(golang(gotest.tools)) = 2.1.0
Provides: bundled(golang(k8s.io/api)) = 1.12.0
Provides: bundled(golang(k8s.io/apimachinery)) = 1.12.0
Provides: bundled(golang(k8s.io/apiserver)) = 1.12.0
Provides: bundled(golang(k8s.io/client-go)) = 1.12.0
Provides: bundled(golang(k8s.io/kubernetes)) = 1.12.0
Provides: bundled(golang(k8s.io/utils)) = cd34563cd63c2bd7c6fe88a73c4dcf34ed8a67cb


%description
containerd is an industry-standard container runtime with an emphasis on
simplicity, robustness and portability. It is available as a daemon for Linux
and Windows, which can manage the complete container lifecycle of its host
system: image transfer and storage, container execution and supervision,
low-level storage and network attachments, etc.


%prep
%autosetup -n containerd-%{version}


%build
mkdir -p src/%(dirname %{import_path})
ln -s ../../.. src/%{import_path}
export GOPATH=$(pwd):%{gopath}
export LDFLAGS="-X %{import_path}/version.Package=%{import_path} -X %{import_path}/version.Version=%{tag} -X %{import_path}/version.Revision=%{commit}"
%gobuild -o bin/containerd %{import_path}/cmd/containerd
%gobuild -o bin/containerd-shim %{import_path}/cmd/containerd-shim
%gobuild -o bin/ctr %{import_path}/cmd/ctr
mkdir man
go-md2man -in src/%{import_path}/docs/man/containerd.1.md -out man/containerd.1
go-md2man -in src/%{import_path}/docs/man/containerd-config.1.md -out man/containerd-config.1
go-md2man -in src/%{import_path}/docs/man/ctr.1.md -out man/ctr.1
go-md2man -in src/%{import_path}/docs/man/containerd-config.toml.5.md -out man/containerd-config.toml.5


%install
install -D -m 0755 bin/containerd %{buildroot}%{_bindir}/containerd
install -D -m 0755 bin/containerd-shim %{buildroot}%{_bindir}/containerd-shim
install -D -m 0755 bin/ctr %{buildroot}%{_bindir}/ctr
install -D -m 0644 man/containerd.1 %{buildroot}%{_mandir}/man1/containerd.1
install -D -m 0644 man/containerd-config.1 %{buildroot}%{_mandir}/man1/containerd-config.1
install -D -m 0644 man/ctr.1 %{buildroot}%{_mandir}/man1/ctr.1
install -D -m 0644 man/containerd-config.toml.5 %{buildroot}%{_mandir}/man5/containerd-config.toml.5
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
%license LICENSE
%doc README.md
%{_bindir}/containerd
%{_bindir}/containerd-shim
%{_bindir}/docker-containerd
%{_bindir}/docker-containerd-shim
%{_bindir}/ctr
%{_unitdir}/containerd.service
%{_mandir}/man1/containerd.1*
%{_mandir}/man1/containerd-config.1*
%{_mandir}/man1/ctr.1*
%{_mandir}/man5/containerd-config.toml.5*
%dir %{_sysconfdir}/containerd
%config(noreplace) %{_sysconfdir}/containerd/config.toml


%changelog
* Thu Oct 25 2018 Carl George <carl@george.computer> - 1.2.0-1
- Latest upstream

* Mon Aug 13 2018 Carl George <carl@george.computer> - 1.1.2-1
- Latest upstream

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 26 2018 Carl George <carl@george.computer> - 1.1.0-1
- Latest upstream
- Build and include man pages

* Wed Apr 04 2018 Carl George <carl@george.computer> - 1.0.3-1
- Latest upstream

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Carl George <carl@george.computer> - 1.0.1-1
- Latest upstream

* Wed Dec 06 2017 Carl George <carl@george.computer> - 1.0.0-1
- Latest upstream

* Fri Nov 10 2017 Carl George <carl@george.computer> - 1.0.0-0.5.beta.3
- Latest upstream

* Thu Oct 19 2017 Carl George <carl@george.computer> - 1.0.0-0.4.beta.2
- Own /etc/containerd

* Thu Oct 12 2017 Carl George <carl@george.computer> - 1.0.0-0.3.beta.2
- Latest upstream
- Require runc 1.0.0 https://github.com/containerd/containerd/issues/1508#issuecomment-335566293

* Mon Oct 09 2017 Carl George <carl@george.computer> - 1.0.0-0.2.beta.1
- Add provides for vendored dependencies
- Add ctr command

* Wed Oct 04 2017 Carl George <carl@george.computer> - 1.0.0-0.1.beta.1
- Initial package
