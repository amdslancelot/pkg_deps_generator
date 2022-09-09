# pkg_info_legal

## Examples

```sh
# ./define_dependency_v2 ~/foreman.spec Requires ./rpm_list_foreman
Dependency: ruby(release),                                   dnf provides: ruby-libs. can't find match from rpm list.                                                                                     
Dependency: rubygems,	 dnf provides: rubygems. can't find match from rpm list.
Dependency: rubygem(rake),	 dnf provides: rubygem-rake. can't find match from rpm list.
Dependency: rubygem(rdoc),	 dnf provides: rubygem-rdoc. can't find match from rpm list.
rubygem-bundler_ext                                          ASL 2.0                      https://github.com/bundlerext/bundler_ext  Requires

...

```


```sh
# ./pkg_info_legal rpm_list_foreman ~/foreman.spec
dnf-plugin-subscription-manager                              GPLv2                        http://www.candlepinproject.org/  no     no                                                                     
dnf-plugin-subscription-manager-debuginfo                    GPLv2                        http://www.candlepinproject.org/  no     no                                                                     
dynflow-utils                                                GPLv3                        https://github.com/dynflow/dynflow  no     no                                                                   
foreman                                                      GPLv3+ with exceptions       https://theforeman.org  Build  Runtime                                                                          
foreman-assets                                               GPLv3+ with exceptions       https://theforeman.org  no     no                                                                               
foreman-bootloaders-redhat                                   GPLv2+ and GPLv3+ and BSD    https://github.com/theforeman/foreman  no     no                                                                
foreman-bootloaders-redhat-tftpboot                          GPLv2+ and GPLv3+ and BSD    https://github.com/theforeman/foreman  no     no                                                                
foreman-build                                                GPLv3+ with exceptions       https://theforeman.org  no     Runtime                                                                          
foreman-cli                                                  GPLv3+ with exceptions       https://theforeman.org  no     no                                                                               
foreman-client-release                                       GPLv3+                       https://theforeman.org  no     no                                                                               
foreman-console                                              GPLv3+ with exceptions       https://theforeman.org  no     no                                                                               
foreman-debug                                                GPLv3+ with exceptions       https://theforeman.org  no     Runtime  

...

```


```sh
# ./pkg_info_legal rpm_list_katello ~/katello.spec libwebsockets-tests-debuginfo
libwebsockets-tests-debuginfo                                LGPLv2 and Public Domain and BSD and MIT and zlib http://libwebsockets.org  no     no                                                       
```
