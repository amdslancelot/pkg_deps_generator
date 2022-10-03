%define debug_package %{nil}

# enable more stripping. This was failing on cisco wrlinux and AIX. We may want
# to get this worked out eventually, but for now let's just skip these for
# those platforms
%global __debug_package %{nil}
# to resolve: "ERROR: No build ID note found"
%undefine _missing_build_ids_terminate_build

# Starting in Fedora 28 and RHEL 8, automatic shebang (#!) munging was added.
# We don't want this in our software and it will interfere with third-party
# dependencies that we don't control. See
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/2PD5RNJRKPN2DVTNGJSBHR5RUSVZSDZI/
# for more info.
%undefine __brp_mangle_shebangs

# Build el-8 packages without build-id files to prevent collision
%define _build_id_links none

# To avoid files installed but not packaged errors
%global __os_install_post %{__os_install_post} \
 rm -rf %{buildroot}/usr/lib/debug

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Name: puppet-agent
Version: 7.18.0
Release: 1%{?dist}
Summary: The Puppet Agent package contains all of the elements needed to run puppet, including ruby, facter, and hiera.
Vendor: Puppet Labs
License: See components
Group: System Environment/Base
URL: https://www.puppetlabs.com

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: %{name}-%{version}.tar.gz
Source1: file-list-for-rpm

# Don't provide anything so the system doesn't use our packages to resolve deps
Autoprov: 0
Autoreq: 0
Requires: findutils
Requires: tar

# All rpm packages built by vanagon have the pre-/post-install script
# boilerplates (defined below). These require `mkdir` and `touch` but previously
# did not specify a dependency on these.
# In the future, we will supress pre/post scripts completely if there's nothing
# specified by the project or the components.
Requires(pre): /bin/mkdir
Requires(pre): /bin/touch
Requires(post): /bin/mkdir
Requires(post): /bin/touch

BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Obsoletes: pe-augeas
Obsoletes: pe-openssl
Obsoletes: pe-ruby
Obsoletes: pe-ruby-mysql
Obsoletes: pe-rubygems
Obsoletes: pe-libyaml
Obsoletes: pe-libldap
Obsoletes: pe-ruby-ldap
Obsoletes: pe-ruby-augeas
Obsoletes: pe-ruby-selinux
Obsoletes: pe-ruby-shadow
Obsoletes: pe-ruby-stomp
Obsoletes: pe-rubygem-deep-merge
Obsoletes: pe-rubygem-net-ssh
Obsoletes: puppet < 4.0.0
Obsoletes: pe-puppet
Obsoletes: pe-ruby-rgen
Obsoletes: pe-cloud-provisioner-libs
Obsoletes: pe-cloud-provisioner
Obsoletes: pe-puppet-enterprise-release < 4.0.0
Obsoletes: pe-agent
Obsoletes: pe-puppetserver-common < 4.0.0
Obsoletes: hiera < 2.0.0
Obsoletes: pe-hiera

Conflicts: pe-r10k < 2.5.0.0

Provides: puppet >= 4.0.0
Provides: hiera >= 2.0.0

%description
The Puppet Agent package contains all of the elements needed to run puppet, including ruby, facter, and hiera.

Contains the following components:
cleanup 
facter 4.2.11
hiera 3.10.0
module-puppetlabs-augeas_core 1.1.2
module-puppetlabs-cron_core 1.0.5
module-puppetlabs-host_core 1.0.3
module-puppetlabs-mount_core 1.0.4
module-puppetlabs-scheduled_task 1.0.0
module-puppetlabs-selinux_core 1.1.0
module-puppetlabs-sshkeys_core 2.2.0
module-puppetlabs-yumrepo_core 1.0.7
module-puppetlabs-zfs_core 1.2.0
module-puppetlabs-zone_core 1.0.3
pl-ruby-patch 
puppet 7.18.0
puppet-resource_api 1.8.14
puppet-runtime 202208121
shellpath 2015-09-18
wrapper-script 

%prep
%setup -q -n %{name}-%{version}

%build

%clean

%install
test -d /opt/freeware/bin && export PATH="/opt/freeware/bin:${PATH}"
rm -rf %{buildroot}
install -d %{buildroot}

# Copy each directory into place. Because empty directories won't make it into.
 if [ -d opt/puppetlabs ]; then
 install -d %{buildroot}/opt
 cp -pr opt/puppetlabs %{buildroot}/opt
 else
 install -d %{buildroot}/opt/puppetlabs
 fi
 if [ -d opt/puppetlabs/puppet ]; then
 install -d %{buildroot}/opt/puppetlabs
 cp -pr opt/puppetlabs/puppet %{buildroot}/opt/puppetlabs
 else
 install -d %{buildroot}/opt/puppetlabs/puppet
 fi
 if [ -d etc/puppetlabs ]; then
 install -d %{buildroot}/etc
 cp -pr etc/puppetlabs %{buildroot}/etc
 else
 install -d %{buildroot}/etc/puppetlabs
 fi
 if [ -d opt/puppetlabs/bin ]; then
 install -d %{buildroot}/opt/puppetlabs
 cp -pr opt/puppetlabs/bin %{buildroot}/opt/puppetlabs
 else
 install -d %{buildroot}/opt/puppetlabs/bin
 fi
 if [ -d var/log/puppetlabs ]; then
 install -d %{buildroot}/var/log
 cp -pr var/log/puppetlabs %{buildroot}/var/log
 else
 install -d %{buildroot}/var/log/puppetlabs
 fi
 if [ -d run/puppetlabs ]; then
 install -d %{buildroot}/run
 cp -pr run/puppetlabs %{buildroot}/run
 else
 install -d %{buildroot}/run/puppetlabs
 fi
 if [ -d opt/puppetlabs/puppet/cache ]; then
 install -d %{buildroot}/opt/puppetlabs/puppet
 cp -pr opt/puppetlabs/puppet/cache %{buildroot}/opt/puppetlabs/puppet
 else
 install -d %{buildroot}/opt/puppetlabs/puppet/cache
 fi
 if [ -d opt/puppetlabs/puppet/public ]; then
 install -d %{buildroot}/opt/puppetlabs/puppet
 cp -pr opt/puppetlabs/puppet/public %{buildroot}/opt/puppetlabs/puppet
 else
 install -d %{buildroot}/opt/puppetlabs/puppet/public
 fi
 if [ -d etc/puppetlabs/puppet ]; then
 install -d %{buildroot}/etc/puppetlabs
 cp -pr etc/puppetlabs/puppet %{buildroot}/etc/puppetlabs
 else
 install -d %{buildroot}/etc/puppetlabs/puppet
 fi
 if [ -d opt/puppetlabs/puppet/share/locale ]; then
 install -d %{buildroot}/opt/puppetlabs/puppet/share
 cp -pr opt/puppetlabs/puppet/share/locale %{buildroot}/opt/puppetlabs/puppet/share
 else
 install -d %{buildroot}/opt/puppetlabs/puppet/share/locale
 fi
 if [ -d etc/puppetlabs/code ]; then
 install -d %{buildroot}/etc/puppetlabs
 cp -pr etc/puppetlabs/code %{buildroot}/etc/puppetlabs
 else
 install -d %{buildroot}/etc/puppetlabs/code
 fi
 if [ -d etc/puppetlabs/code/modules ]; then
 install -d %{buildroot}/etc/puppetlabs/code
 cp -pr etc/puppetlabs/code/modules %{buildroot}/etc/puppetlabs/code
 else
 install -d %{buildroot}/etc/puppetlabs/code/modules
 fi
 if [ -d opt/puppetlabs/puppet/modules ]; then
 install -d %{buildroot}/opt/puppetlabs/puppet
 cp -pr opt/puppetlabs/puppet/modules %{buildroot}/opt/puppetlabs/puppet
 else
 install -d %{buildroot}/opt/puppetlabs/puppet/modules
 fi
 if [ -d etc/puppetlabs/code/environments ]; then
 install -d %{buildroot}/etc/puppetlabs/code
 cp -pr etc/puppetlabs/code/environments %{buildroot}/etc/puppetlabs/code
 else
 install -d %{buildroot}/etc/puppetlabs/code/environments
 fi
 if [ -d etc/puppetlabs/code/environments/production ]; then
 install -d %{buildroot}/etc/puppetlabs/code/environments
 cp -pr etc/puppetlabs/code/environments/production %{buildroot}/etc/puppetlabs/code/environments
 else
 install -d %{buildroot}/etc/puppetlabs/code/environments/production
 fi
 if [ -d etc/puppetlabs/code/environments/production/manifests ]; then
 install -d %{buildroot}/etc/puppetlabs/code/environments/production
 cp -pr etc/puppetlabs/code/environments/production/manifests %{buildroot}/etc/puppetlabs/code/environments/production
 else
 install -d %{buildroot}/etc/puppetlabs/code/environments/production/manifests
 fi
 if [ -d etc/puppetlabs/code/environments/production/modules ]; then
 install -d %{buildroot}/etc/puppetlabs/code/environments/production
 cp -pr etc/puppetlabs/code/environments/production/modules %{buildroot}/etc/puppetlabs/code/environments/production
 else
 install -d %{buildroot}/etc/puppetlabs/code/environments/production/modules
 fi
 if [ -d etc/puppetlabs/code/environments/production/data ]; then
 install -d %{buildroot}/etc/puppetlabs/code/environments/production
 cp -pr etc/puppetlabs/code/environments/production/data %{buildroot}/etc/puppetlabs/code/environments/production
 else
 install -d %{buildroot}/etc/puppetlabs/code/environments/production/data
 fi
 if [ -d var/log/puppetlabs/puppet ]; then
 install -d %{buildroot}/var/log/puppetlabs
 cp -pr var/log/puppetlabs/puppet %{buildroot}/var/log/puppetlabs
 else
 install -d %{buildroot}/var/log/puppetlabs/puppet
 fi
 if [ -d opt/puppetlabs/facter/facts.d ]; then
 install -d %{buildroot}/opt/puppetlabs/facter
 cp -pr opt/puppetlabs/facter/facts.d %{buildroot}/opt/puppetlabs/facter
 else
 install -d %{buildroot}/opt/puppetlabs/facter/facts.d
 fi
 if [ -d opt/puppetlabs/puppet/vendor_modules ]; then
 install -d %{buildroot}/opt/puppetlabs/puppet
 cp -pr opt/puppetlabs/puppet/vendor_modules %{buildroot}/opt/puppetlabs/puppet
 else
 install -d %{buildroot}/opt/puppetlabs/puppet/vendor_modules
 fi

# Copy each of the extra files into place
 install -d %{buildroot}/opt/puppetlabs/puppet
 cp -Rp opt/puppetlabs/puppet/VERSION %{buildroot}/opt/puppetlabs/puppet
 install -d %{buildroot}/usr/lib/systemd/system
 cp -Rp usr/lib/systemd/system/puppet.service %{buildroot}/usr/lib/systemd/system
 install -d %{buildroot}/opt/puppetlabs/puppet/bin
 cp -Rp opt/puppetlabs/puppet/bin/eyaml %{buildroot}/opt/puppetlabs/puppet/bin
 install -d %{buildroot}/opt/puppetlabs/puppet/lib/ruby/gems/2.7.0/specifications
 cp -Rp opt/puppetlabs/puppet/lib/ruby/gems/2.7.0/specifications/puppet-7.18.0.gemspec %{buildroot}/opt/puppetlabs/puppet/lib/ruby/gems/2.7.0/specifications
 install -d %{buildroot}/opt/puppetlabs/puppet/lib/ruby/gems/2.7.0/specifications
 cp -Rp opt/puppetlabs/puppet/lib/ruby/gems/2.7.0/specifications/facter-4.2.11.gemspec %{buildroot}/opt/puppetlabs/puppet/lib/ruby/gems/2.7.0/specifications
 install -d %{buildroot}/opt/puppetlabs/puppet/lib/ruby/gems/2.7.0/specifications
 cp -Rp opt/puppetlabs/puppet/lib/ruby/gems/2.7.0/specifications/hiera-3.10.0.gemspec %{buildroot}/opt/puppetlabs/puppet/lib/ruby/gems/2.7.0/specifications
 install -d %{buildroot}/etc/profile.d
 cp -Rp etc/profile.d/puppet-agent.sh %{buildroot}/etc/profile.d
 install -d %{buildroot}/etc/profile.d
 cp -Rp etc/profile.d/puppet-agent.csh %{buildroot}/etc/profile.d
 install -d %{buildroot}/opt/puppetlabs/puppet/bin
 cp -Rp opt/puppetlabs/puppet/bin/wrapper.sh %{buildroot}/opt/puppetlabs/puppet/bin
 install -d %{buildroot}/opt/puppetlabs/bin
 cp -Rp opt/puppetlabs/bin/facter %{buildroot}/opt/puppetlabs/bin
 install -d %{buildroot}/opt/puppetlabs/bin
 cp -Rp opt/puppetlabs/bin/hiera %{buildroot}/opt/puppetlabs/bin
 install -d %{buildroot}/opt/puppetlabs/bin
 cp -Rp opt/puppetlabs/bin/puppet %{buildroot}/opt/puppetlabs/bin
 install -d %{buildroot}/opt/puppetlabs/bin
 cp -Rp opt/puppetlabs/bin/pxp-agent %{buildroot}/opt/puppetlabs/bin
 install -d %{buildroot}/etc/sysconfig
 cp -Rp etc/sysconfig/puppet %{buildroot}/etc/sysconfig
 install -d %{buildroot}/usr/lib/tmpfiles.d
 cp -Rp usr/lib/tmpfiles.d/puppet-agent.conf %{buildroot}/usr/lib/tmpfiles.d
 install -d %{buildroot}/opt/puppetlabs/puppet/share/vim/puppet-vimfiles/ftdetect
 cp -Rp opt/puppetlabs/puppet/share/vim/puppet-vimfiles/ftdetect/puppet.vim %{buildroot}/opt/puppetlabs/puppet/share/vim/puppet-vimfiles/ftdetect
 install -d %{buildroot}/opt/puppetlabs/puppet/share/vim/puppet-vimfiles/ftplugin
 cp -Rp opt/puppetlabs/puppet/share/vim/puppet-vimfiles/ftplugin/puppet.vim %{buildroot}/opt/puppetlabs/puppet/share/vim/puppet-vimfiles/ftplugin
 install -d %{buildroot}/opt/puppetlabs/puppet/share/vim/puppet-vimfiles/indent
 cp -Rp opt/puppetlabs/puppet/share/vim/puppet-vimfiles/indent/puppet.vim %{buildroot}/opt/puppetlabs/puppet/share/vim/puppet-vimfiles/indent
 install -d %{buildroot}/opt/puppetlabs/puppet/share/vim/puppet-vimfiles/syntax
 cp -Rp opt/puppetlabs/puppet/share/vim/puppet-vimfiles/syntax/puppet.vim %{buildroot}/opt/puppetlabs/puppet/share/vim/puppet-vimfiles/syntax
 install -d %{buildroot}/etc/puppetlabs/puppet
 cp -Rp etc/puppetlabs/puppet/puppet.conf %{buildroot}/etc/puppetlabs/puppet
 install -d %{buildroot}/etc/puppetlabs/code/environments/production
 cp -Rp etc/puppetlabs/code/environments/production/environment.conf %{buildroot}/etc/puppetlabs/code/environments/production
 install -d %{buildroot}/etc/puppetlabs/code/environments/production
 cp -Rp etc/puppetlabs/code/environments/production/hiera.yaml %{buildroot}/etc/puppetlabs/code/environments/production
 install -d %{buildroot}/etc/puppetlabs/puppet
 cp -Rp etc/puppetlabs/puppet/hiera.yaml %{buildroot}/etc/puppetlabs/puppet

# Here we explicitly remove the directories and files that we list in the
# %files section separately because rpm3 on aix errors on duplicate files in
# the package.
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/puppet$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/etc/puppetlabs$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/bin$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/var/log/puppetlabs$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/run/puppetlabs$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/puppet/cache$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/puppet/public$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/etc/puppetlabs/puppet$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/puppet/share/locale$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/etc/puppetlabs/code$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/etc/puppetlabs/code/modules$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/puppet/modules$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/etc/puppetlabs/code/environments$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/etc/puppetlabs/code/environments/production$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/etc/puppetlabs/code/environments/production/manifests$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/etc/puppetlabs/code/environments/production/modules$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/etc/puppetlabs/code/environments/production/data$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/var/log/puppetlabs/puppet$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/facter/facts.d$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/puppet/vendor_modules$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/puppet/VERSION$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/usr/lib/systemd/system/puppet.service$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/puppet/bin/eyaml$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/puppet/lib/ruby/gems/2.7.0/specifications/puppet-7.18.0.gemspec$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/puppet/lib/ruby/gems/2.7.0/specifications/facter-4.2.11.gemspec$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/puppet/lib/ruby/gems/2.7.0/specifications/hiera-3.10.0.gemspec$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/etc/profile.d/puppet-agent.sh$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/etc/profile.d/puppet-agent.csh$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/puppet/bin/wrapper.sh$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/bin/facter$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/bin/hiera$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/bin/puppet$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/bin/pxp-agent$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/etc/sysconfig/puppet$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/usr/lib/tmpfiles.d/puppet-agent.conf$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/puppet/share/vim/puppet-vimfiles/ftdetect/puppet.vim$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/puppet/share/vim/puppet-vimfiles/ftplugin/puppet.vim$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/puppet/share/vim/puppet-vimfiles/indent/puppet.vim$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/opt/puppetlabs/puppet/share/vim/puppet-vimfiles/syntax/puppet.vim$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/etc/puppetlabs/puppet/puppet.conf$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/etc/puppetlabs/code/environments/production/environment.conf$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/etc/puppetlabs/code/environments/production/hiera.yaml$||g' %{SOURCE1}
 PATH=/opt/freeware/bin:$PATH sed -i 's|^/etc/puppetlabs/puppet/hiera.yaml$||g' %{SOURCE1}

# Here we turn all dirs in the file-list into %dir entries to avoid duplicate files
if command -v perl; then
 perl -i -lne 'if ((-d $_) && !(-l $_)) { print "%dir $_" } else { print }' %{SOURCE1}
else
 while read entry; do
 if [ -n "$entry" -a -d "$entry" -a ! -L "$entry" ]; then
 sed -i "\|^$entry\$|s|^|%dir |" %{SOURCE1}
 fi
 done < %{SOURCE1}
fi

%pre
# Save state so we know later if this is an upgrade or an install
mkdir -p %{_localstatedir}/lib/rpm-state/%{name}
if [ "$1" -eq 1 ] ; then
 touch %{_localstatedir}/lib/rpm-state/%{name}/install
fi
if [ "$1" -gt 1 ] ; then
 touch %{_localstatedir}/lib/rpm-state/%{name}/upgrade
fi

# Run preinstall scripts on install if defined
if [ "$1" -eq 1 ] ; then
 : no preinstall scripts provided
fi

# Run preinstall scripts on upgrade if defined
if [ "$1" -gt 1 ] ; then
 # Backup the old hiera configs if present, so that we
# can drop them back in place if the package manager
# tries to remove it.
if [ -e /etc/puppetlabs/code/hiera.yaml ]; then
 cp -a /etc/puppetlabs/code/hiera.yaml{,.pkg-old}
 touch /etc/puppetlabs/puppet/remove_hiera5_files.rm
fi
if [ -e /etc/puppetlabs/puppet/hiera.yaml ]; then
 cp -a /etc/puppetlabs/puppet/hiera.yaml{,.pkg-old}
 touch /etc/puppetlabs/puppet/remove_hiera5_files.rm
fi
if [ -e /etc/puppetlabs/code/environments/production/hiera.yaml ]; then
 cp -a /etc/puppetlabs/code/environments/production/hiera.yaml{,.pkg-old}
 touch /etc/puppetlabs/puppet/remove_hiera5_files.rm
fi

fi

%post
 # switch based on systemd vs systemv vs smf vs aix
 #
 %systemd_post puppet.service

%triggerpostun -- puppet-agent

%postun
# Run post-uninstall scripts on upgrade if defined
if [ "$1" -eq 1 ] ; then
 : no postremove scripts provided
fi

# Run post-uninstall scripts on removal if defined
if [ "$1" -eq 0 ] ; then
 : no postremove scripts provided
fi

 # switch based on systemd vs systemv vs smf vs aix
 #
 %systemd_postun_with_restart puppet.service

%preun
# Run pre-uninstall scripts on upgrade if defined
if [ "$1" -eq 1 ] ; then
 : no preremove scripts provided
fi

# Run pre-uninstall scripts on removal if defined
if [ "$1" -eq 0 ] ; then
 : no preremove scripts provided
fi

 %systemd_preun puppet.service

%posttrans
# Run post-transaction scripts on install if defined
if [ -e %{_localstatedir}/lib/rpm-state/%{name}/install ] ; then
 : no postinstall scripts provided
 rm %{_localstatedir}/lib/rpm-state/%{name}/install
fi

# Run post-transaction scripts on upgrade if defined
if [ -e %{_localstatedir}/lib/rpm-state/%{name}/upgrade ] ; then
 # Remove any extra hiera config files we laid down if prev config present
if [ -e /etc/puppetlabs/puppet/remove_hiera5_files.rm ]; then
 rm -f /etc/puppetlabs/puppet/hiera.yaml
 rm -f /etc/puppetlabs/code/environments/production/hiera.yaml
 rm -f /etc/puppetlabs/puppet/remove_hiera5_files.rm
fi

# Restore the old hiera, if it existed
if [ -e /etc/puppetlabs/code/hiera.yaml.pkg-old ]; then
 mv /etc/puppetlabs/code/hiera.yaml{.pkg-old,}
fi
if [ -e /etc/puppetlabs/puppet/hiera.yaml.pkg-old ]; then
 mv /etc/puppetlabs/puppet/hiera.yaml{.pkg-old,}
fi
if [ -e /etc/puppetlabs/code/environments/production/hiera.yaml.pkg-old ]; then
 mv /etc/puppetlabs/code/environments/production/hiera.yaml{.pkg-old,}
fi

 rm %{_localstatedir}/lib/rpm-state/%{name}/upgrade
fi

%files -f %{SOURCE1}
%doc bill-of-materials
%defattr(-, root, root, 0755)
%dir %attr(-, -, -) /opt/puppetlabs
%dir %attr(-, -, -) /opt/puppetlabs/puppet
%dir %attr(-, -, -) /etc/puppetlabs
%dir %attr(-, -, -) /opt/puppetlabs/bin
%dir %attr(-, -, -) /var/log/puppetlabs
%dir %attr(-, -, -) /run/puppetlabs
%dir %attr(0750, -, -) /opt/puppetlabs/puppet/cache
%dir %attr(0755, -, -) /opt/puppetlabs/puppet/public
%dir %attr(-, -, -) /etc/puppetlabs/puppet
%dir %attr(-, -, -) /opt/puppetlabs/puppet/share/locale
%dir %attr(-, -, -) /etc/puppetlabs/code
%dir %attr(-, -, -) /etc/puppetlabs/code/modules
%dir %attr(-, -, -) /opt/puppetlabs/puppet/modules
%dir %attr(-, -, -) /etc/puppetlabs/code/environments
%dir %attr(-, -, -) /etc/puppetlabs/code/environments/production
%dir %attr(-, -, -) /etc/puppetlabs/code/environments/production/manifests
%dir %attr(-, -, -) /etc/puppetlabs/code/environments/production/modules
%dir %attr(-, -, -) /etc/puppetlabs/code/environments/production/data
%dir %attr(0750, -, -) /var/log/puppetlabs/puppet
%dir %attr(-, -, -) /opt/puppetlabs/facter/facts.d
%dir %attr(0755, root, root) /opt/puppetlabs/puppet/vendor_modules
%config(noreplace) %attr(-, -, -) /etc/sysconfig/puppet
%config(noreplace) %attr(0644, -, -) /usr/lib/tmpfiles.d/puppet-agent.conf
%config(noreplace) %attr(0644, -, -) /opt/puppetlabs/puppet/share/vim/puppet-vimfiles/ftdetect/puppet.vim
%config(noreplace) %attr(0644, -, -) /opt/puppetlabs/puppet/share/vim/puppet-vimfiles/ftplugin/puppet.vim
%config(noreplace) %attr(0644, -, -) /opt/puppetlabs/puppet/share/vim/puppet-vimfiles/indent/puppet.vim
%config(noreplace) %attr(0644, -, -) /opt/puppetlabs/puppet/share/vim/puppet-vimfiles/syntax/puppet.vim
%config(noreplace) %attr(-, -, -) /etc/puppetlabs/puppet/puppet.conf
%config(noreplace) %attr(0644, -, -) /etc/puppetlabs/code/environments/production/environment.conf
%config(noreplace) %attr(-, -, -) /etc/puppetlabs/code/environments/production/hiera.yaml
%config(noreplace) %attr(-, -, -) /etc/puppetlabs/puppet/hiera.yaml
%attr(-, -, -) /opt/puppetlabs/puppet/VERSION
%attr(0644, -, -) /usr/lib/systemd/system/puppet.service
%attr(-, -, -) /opt/puppetlabs/puppet/bin/eyaml
%attr(0644, -, -) /opt/puppetlabs/puppet/lib/ruby/gems/2.7.0/specifications/puppet-7.18.0.gemspec
%attr(0644, -, -) /opt/puppetlabs/puppet/lib/ruby/gems/2.7.0/specifications/facter-4.2.11.gemspec
%attr(0644, -, -) /opt/puppetlabs/puppet/lib/ruby/gems/2.7.0/specifications/hiera-3.10.0.gemspec
%attr(0644, -, -) /etc/profile.d/puppet-agent.sh
%attr(0644, -, -) /etc/profile.d/puppet-agent.csh
%attr(0755, -, -) /opt/puppetlabs/puppet/bin/wrapper.sh
%attr(-, -, -) /opt/puppetlabs/bin/facter
%attr(-, -, -) /opt/puppetlabs/bin/hiera
%attr(-, -, -) /opt/puppetlabs/bin/puppet
%attr(-, -, -) /opt/puppetlabs/bin/pxp-agent

%changelog
* Fri Sep 23 2022 Puppet Labs <info@puppetlabs.com> - 7.18.0-1
- Build for 7.18.0-1
