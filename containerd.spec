%define _libexecdir /usr/libexec
%define debugcflags %nil

# modifying the dockerinit binary breaks the SHA1 sum check by docker
#global __os_install_post %{_usrlibrpm}/brp-compress

#debuginfo not supported with Go
%global debug_package %{nil}
%global import_path github.com/docker/containerd
%global go_dir  %{_libdir}/go
%define gosrc %{go_dir}/src/%{import_path}
%define provider github
%define provider_tld com
%define project %{name}
%define	shortcommit 4dc5990

Name:           containerd
Version:        0.2.2
Release:        2
Summary:        Daemon to control runC
License:        ASL 2.0
Group:		System/Base
URL:            http://containerd.tools
Source0:        https://%{import_path}/archive/v%{version}.tar.gz
BuildRequires:  glibc-static-devel

BuildRequires:  golang
BuildRequires:  pkgconfig(sqlite3)

BuildRequires:  go-md2man
BuildRequires:  pkgconfig(systemd)
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	btrfs-devel
Requires:       systemd

# need xz to work with ubuntu images
# https://bugzilla.redhat.com/show_bug.cgi?id=1045220
Requires:       xz
# https://bugzilla.redhat.com/show_bug.cgi?id=1034919
# No longer needed in Fedora because of libcontainer
Requires:       libcgroup
Requires:	e2fsprogs
Requires:	iptables

Requires:	runc

%description
Containerd is a daemon with an API and a command line client, to manage
containers on one machine.

It uses runC to run containers according to the OCI specification.
Containerd has advanced features such as seccomp and user namespace
support as well as checkpoint and restore for cloning and live migration
of containers.

%package devel
BuildRequires:  golang >= 1.3.3
Requires:       golang >= 1.3.3
Summary:        A golang registry for global request variables (source libraries)
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/api) = %{version}-%{release}
Provides:       golang(%{import_path}/api/client) = %{version}-%{release}
Provides:       golang(%{import_path}/api/server) = %{version}-%{release}
Provides:       golang(%{import_path}/api/types) = %{version}-%{release}
Provides:       golang(%{import_path}/archive) = %{version}-%{release}
Provides:       golang(%{import_path}/builtins) = %{version}-%{release}
Provides:       golang(%{import_path}/contrib) = %{version}-%{release}
Provides:       golang(%{import_path}/contrib/docker-device-tool) = %{version}-%{release}
Provides:       golang(%{import_path}/contrib/host-integration) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/execdrivers) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/lxc) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/native) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/native/template) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/aufs) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/btrfs) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/devmapper) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/overlay) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/graphtest) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/vfs) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/logger) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/logger/jsonfilelog) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/logger/syslog) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/bridge) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/ipallocator) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/portallocator) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/portmapper) = %{version}-%{release}
Provides:       golang(%{import_path}/dockerversion) = %{version}-%{release}
Provides:       golang(%{import_path}/engine) = %{version}-%{release}
Provides:       golang(%{import_path}/graph) = %{version}-%{release}
Provides:       golang(%{import_path}/image) = %{version}-%{release}
Provides:       golang(%{import_path}/integration) = %{version}-%{release}
Provides:       golang(%{import_path}/integration-cli) = %{version}-%{release}
Provides:       golang(%{import_path}/links) = %{version}-%{release}
Provides:       golang(%{import_path}/nat) = %{version}-%{release}
Provides:       golang(%{import_path}/opts) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/term) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/term/winconsole) = %{version}-%{release}
Provides:       golang(%{import_path}/registry) = %{version}-%{release}
Provides:       golang(%{import_path}/registry/v2) = %{version}-%{release}
Provides:       golang(%{import_path}/runconfig) = %{version}-%{release}
Provides:       golang(%{import_path}/utils) = %{version}-%{release}
Provides:       golang(%{import_path}/utils/broadcastwriter) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/graphdb) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/iptables) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/listenbuffer) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/mflag) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/mflag/example) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/mount) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/namesgenerator) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/networkfs/etchosts) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/networkfs/resolvconf) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/proxy) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/signal) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/symlink) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/sysinfo) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/system) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/systemd) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/tailfile) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/term) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/testutils) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/truncindex) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/units) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/user) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/version) = %{version}-%{release}

%description devel
This is the source libraries for docker.

%prep
%setup -q
%apply_patches
#rm -rf vendor/src/code.google.com vendor/src/github.com/{coreos,docker/libtrust,godbus,gorilla,kr,syndtr,tchap}
#for f in `find . -name '*.go'`; do
	#perl -pi -e 's|github.com/docker/docker/vendor/src/code.google.com/p/go/src/pkg/archive/tar|archive/tar|' $f
#done

%build
#export CC=gcc
#export CXX=g++
#sed -i 's!external!internal!g' hack/make.sh
#mkdir -p bfd
#ln -s %{_bindir}/ld.bfd bfd/ld
#export PATH=$PWD/bfd:$PATH
#export DOCKER_GITCOMMIT="%{shortcommit}"
#export CGO_CFLAGS="-I%{_includedir}"
#export CGO_LDFLAGS="-L%{_libdir}"
#export AUTO_GOPATH=1

# FIXME there must be a better way to make go see those?!
mkdir -p vendor/src/github.com/docker/containerd
for i in *; do
	[ -d $i ] && ln -s `pwd`/$i vendor/src/github.com/docker/containerd/
done
cat >vendor/src/github.com/docker/containerd/version.go <<'EOF'
package containerd;
const Version = "%{version}";
const GitCommit = "1234567890";
EOF

GOPATH=`pwd` make

%install
# install binary
install -d %{buildroot}%{_bindir}
install -p -m 755 bin/* %{buildroot}%{_bindir}/

# install systemd/init scripts
install -d %{buildroot}%{_unitdir}
sed -e 's,/usr/local,%{_prefix},g' hack/containerd.service >%{buildroot}%{_unitdir}/containerd.service

# sources
install -d -p %{buildroot}/%{gosrc}

for dir in api containerd containerd-shim ctr osutils runtime specs supervisor
do
	cp -rpav $dir %{buildroot}/%{gosrc}
done

find %{buildroot} -name "*~" -exec rm -rf {} \;
find %{buildroot}%{go_dir}/src/github.com/ -type d -exec chmod 0755 {} \;

# Docker expects stuff to be named its way...
cd %{buildroot}%{_bindir}
for i in *; do
	ln -s $i docker-$i
done

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-containerd.preset << EOF
enable containerd.service
EOF

%files
%doc MAINTAINERS NOTICE README.md 
%{_bindir}/containerd
%{_bindir}/containerd-shim
%{_bindir}/ctr
%{_bindir}/docker-containerd
%{_bindir}/docker-containerd-shim
%{_bindir}/docker-ctr
%{_presetdir}/86-containerd.preset
%{_unitdir}/containerd.service

%files devel
%doc MAINTAINERS NOTICE README.md
%{go_dir}/src/github.com
