#!/bin/bash

# Allows ssh without password
# ssh-keygen -f "/home/anmol/.ssh/known_hosts" -R 10.129.2.110
# ssh ubuntu64@10.129.2.110 mkdir -p .ssh
# cat .ssh/id_rsa.pub | ssh ubuntu64@10.129.2.110 'cat >> .ssh/authorized_keys'

# ssh-keygen -f "/home/anmol/.ssh/known_hosts" -R 10.129.2.111
# ssh ubuntu64@10.129.2.111 mkdir -p .ssh
# cat .ssh/id_rsa.pub | ssh ubuntu64@10.129.2.111 'cat >> .ssh/authorized_keys'

# ssh-keygen -f "/home/anmol/.ssh/known_hosts" -R 10.129.2.112
# ssh ubuntu64@10.129.2.112 mkdir -p .ssh
# cat .ssh/id_rsa.pub | ssh ubuntu64@10.129.2.112 'cat >> .ssh/authorized_keys'

# ssh-keygen -f "/home/anmol/.ssh/known_hosts" -R 10.129.2.113
# ssh ubuntu64@10.129.2.113 mkdir -p .ssh
# cat .ssh/id_rsa.pub | ssh ubuntu64@10.129.2.113 'cat >> .ssh/authorized_keys'

# ssh-keygen -f "/home/anmol/.ssh/known_hosts" -R 10.129.2.114
# ssh ubuntu64@10.129.2.114 mkdir -p .ssh
# cat .ssh/id_rsa.pub | ssh ubuntu64@10.129.2.114 'cat >> .ssh/authorized_keys'

# ssh-keygen -f "/home/anmol/.ssh/known_hosts" -R 10.129.2.115
# ssh ubuntu64@10.129.2.115 mkdir -p .ssh
# cat .ssh/id_rsa.pub | ssh ubuntu64@10.129.2.115 'cat >> .ssh/authorized_keys'

# ssh-keygen -f "/home/anmol/.ssh/known_hosts" -R 10.129.2.116
# ssh ubuntu64@10.129.2.116 mkdir -p .ssh
# cat .ssh/id_rsa.pub | ssh ubuntu64@10.129.2.116 'cat >> .ssh/authorized_keys'

# Copy proxy setting script

 scp port.sh ubuntu64@10.129.2.110:~/
 scp port.sh ubuntu64@10.129.2.111:~/
 scp port.sh ubuntu64@10.129.2.112:~/
 scp port.sh ubuntu64@10.129.2.113:~/
 scp port.sh ubuntu64@10.129.2.114:~/
 scp port.sh ubuntu64@10.129.2.115:~/
 scp port.sh ubuntu64@10.129.2.116:~/

# run a sudo apt-get update on all the VM's

# ssh -t ubuntu64@10.129.2.110 './proxy.sh; sudo apt-get update; logout' 

# ssh -t ubuntu64@10.129.2.111 './proxy.sh; sudo apt-get update; logout' 

# ssh -t ubuntu64@10.129.2.112 './proxy.sh; sudo apt-get update; logout' 

# ssh -t ubuntu64@10.129.2.113 './proxy.sh; sudo apt-get update; logout' 

# ssh -t ubuntu64@10.129.2.114 './proxy.sh; sudo apt-get update; logout' 

# ssh -t ubuntu64@10.129.2.115 './proxy.sh; sudo apt-get update; logout' 

# ssh -t ubuntu64@10.129.2.116 './proxy.sh; sudo apt-get update; logout' 

# Configuring the APT software sources

# scp repo_key ubuntu64@10.129.2.110:~/

# ssh -t ubuntu64@10.129.2.110 'sudo touch /etc/apt/sources.list.d/clearwater.list;

# echo "deb http://repo.cw-ngv.com/stable binary/" | sudo tee /etc/apt/sources.list.d/clearwater.list;

# sudo apt-key add ~/repo_key;

# sudo apt-get update;
# ' 


# scp repo_key ubuntu64@10.129.2.111:~/

# ssh -t ubuntu64@10.129.2.111 'sudo touch /etc/apt/sources.list.d/clearwater.list;

# echo "deb http://repo.cw-ngv.com/stable binary/" | sudo tee /etc/apt/sources.list.d/clearwater.list;

# sudo apt-key add ~/repo_key;

# sudo apt-get update;
# ' 


# scp repo_key ubuntu64@10.129.2.112:~/

# ssh -t ubuntu64@10.129.2.112 'sudo touch /etc/apt/sources.list.d/clearwater.list;

# echo "deb http://repo.cw-ngv.com/stable binary/" | sudo tee /etc/apt/sources.list.d/clearwater.list;

# sudo apt-key add ~/repo_key;

# sudo apt-get update;
# ' 


# scp repo_key ubuntu64@10.129.2.118:~/

# ssh -t ubuntu64@10.129.2.118 'sudo touch /etc/apt/sources.list.d/clearwater.list;

# echo "deb http://repo.cw-ngv.com/stable binary/" | sudo tee /etc/apt/sources.list.d/clearwater.list;

# sudo apt-key add ~/repo_key;

# sudo apt-get update;
# ' 

# scp repo_key ubuntu64@10.129.2.114:~/

# ssh -t ubuntu64@10.129.2.114 'sudo touch /etc/apt/sources.list.d/clearwater.list;

# echo "deb http://repo.cw-ngv.com/stable binary/" | sudo tee /etc/apt/sources.list.d/clearwater.list;

# sudo apt-key add ~/repo_key;

# sudo apt-get update;
# ' 

# scp repo_key ubuntu64@10.129.2.115:~/

# ssh -t ubuntu64@10.129.2.115 'sudo touch /etc/apt/sources.list.d/clearwater.list;

# echo "deb http://repo.cw-ngv.com/stable binary/" | sudo tee /etc/apt/sources.list.d/clearwater.list;

# sudo apt-key add ~/repo_key;

# sudo apt-get update;
# ' 


# scp repo_key ubuntu64@10.129.2.116:~/

# ssh -t ubuntu64@10.129.2.116 'sudo touch /etc/apt/sources.list.d/clearwater.list;

# echo "deb http://repo.cw-ngv.com/stable binary/" | sudo tee /etc/apt/sources.list.d/clearwater.list;

# sudo apt-key add ~/repo_key;

# sudo apt-get update;
# ' 

# Configuring the inter-node hostnames/IP addresses

# ssh -t ubuntu64@10.129.2.110 'sudo mkdir -p /etc/clearwater;

# sudo touch /etc/clearwater/config;

# echo "
# # Deployment definitions
# home_domain=ims.hom
# sprout_hostname=sprout.ims.hom
# chronos_hostname=10.129.2.110:7253
# hs_hostname=hs.ims.hom:8888
# hs_provisioning_hostname=hs.ims.hom:8889
# ralf_hostname=ralf.ims.hom:10888
# xdms_hostname=homer.ims.hom:7888

# # Local IP configuration
# local_ip=10.129.2.110
# public_ip=10.129.2.110
# public_hostname=dns-1

# # Email server configuration
# # smtp_smarthost=<smtp server>
# # smtp_username=<username>
# # smtp_password=<password>
# # email_recovery_sender=clearwater@example.org

# # Keys
# signup_key=secret
# turn_workaround=secret
# ellis_api_key=secret
# ellis_cookie_key=secret" | sudo tee /etc/clearwater/config;
# '

# ssh -t ubuntu64@10.129.2.111 'sudo touch /etc/clearwater/config;

# echo "
# # Deployment definitions
# home_domain=ims.hom
# sprout_hostname=sprout.ims.hom
# chronos_hostname=10.129.2.111:7253
# hs_hostname=hs.ims.hom:8888
# hs_provisioning_hostname=hs.ims.hom:8889
# ralf_hostname=ralf.ims.hom:10888
# xdms_hostname=homer.ims.hom:7888

# # Local IP configuration
# local_ip=10.129.2.111
# public_ip=10.129.2.111
# public_hostname=bono-1

# # Email server configuration
# # smtp_smarthost=<smtp server>
# # smtp_username=<username>
# # smtp_password=<password>
# # email_recovery_sender=clearwater@example.org

# # Keys
# signup_key=secret
# turn_workaround=secret
# ellis_api_key=secret
# ellis_cookie_key=secret" | sudo tee /etc/clearwater/config;
# '


# ssh -t ubuntu64@10.129.2.112 'sudo touch /etc/clearwater/config;

# echo "
# # Deployment definitions
# home_domain=ims.hom
# sprout_hostname=sprout.ims.hom
# chronos_hostname=10.129.2.112:7253
# hs_hostname=hs.ims.hom:8888
# hs_provisioning_hostname=hs.ims.hom:8889
# ralf_hostname=ralf.ims.hom:10888
# xdms_hostname=homer.ims.hom:7888

# # Local IP configuration
# local_ip=10.129.2.112
# public_ip=10.129.2.112
# public_hostname=sprout-1

# # Email server configuration
# # smtp_smarthost=<smtp server>
# # smtp_username=<username>
# # smtp_password=<password>
# # email_recovery_sender=clearwater@example.org

# # Keys
# signup_key=secret
# turn_workaround=secret
# ellis_api_key=secret
# ellis_cookie_key=secret" | sudo tee /etc/clearwater/config;
# '

# ssh -t ubuntu64@10.129.2.118 'sudo mkdir -p /etc/clearwater;

# sudo touch /etc/clearwater/config;

# echo "
# # Deployment definitions
# home_domain=ims.hom
# sprout_hostname=sprout.ims.hom
# chronos_hostname=10.129.2.118:7253
# hs_hostname=hs.ims.hom:8888
# hs_provisioning_hostname=hs.ims.hom:8889
# ralf_hostname=ralf.ims.hom:10888
# xdms_hostname=homer.ims.hom:7888

# # Local IP configuration
# local_ip=10.129.2.118
# public_ip=10.129.2.118
# public_hostname=homestead-1

# # Email server configuration
# # smtp_smarthost=<smtp server>
# # smtp_username=<username>
# # smtp_password=<password>
# # email_recovery_sender=clearwater@example.org

# # Keys
# signup_key=secret
# turn_workaround=secret
# ellis_api_key=secret
# ellis_cookie_key=secret" | sudo tee /etc/clearwater/config;
# '

# ssh -t ubuntu64@10.129.2.114 'sudo mkdir -p /etc/clearwater;

# sudo touch /etc/clearwater/config;

# echo "
# # Deployment definitions
# home_domain=ims.hom
# sprout_hostname=sprout.ims.hom
# chronos_hostname=10.129.2.114:7253
# hs_hostname=hs.ims.hom:8888
# hs_provisioning_hostname=hs.ims.hom:8889
# ralf_hostname=ralf.ims.hom:10888
# xdms_hostname=homer.ims.hom:7888

# # Local IP configuration
# local_ip=10.129.2.114
# public_ip=10.129.2.114
# public_hostname=homer-1

# # Email server configuration
# # smtp_smarthost=<smtp server>
# # smtp_username=<username>
# # smtp_password=<password>
# # email_recovery_sender=clearwater@example.org

# # Keys
# signup_key=secret
# turn_workaround=secret
# ellis_api_key=secret
# ellis_cookie_key=secret" | sudo tee /etc/clearwater/config;
# '

# ssh -t ubuntu64@10.129.2.115 'sudo touch /etc/clearwater/config;

# echo "
# # Deployment definitions
# home_domain=ims.hom
# sprout_hostname=sprout.ims.hom
# chronos_hostname=10.129.2.115:7253
# hs_hostname=hs.ims.hom:8888
# hs_provisioning_hostname=hs.ims.hom:8889
# ralf_hostname=ralf.ims.hom:10888
# xdms_hostname=homer.ims.hom:7888

# # Local IP configuration
# local_ip=10.129.2.115
# public_ip=10.129.2.115
# public_hostname=ralf-1

# # Email server configuration
# # smtp_smarthost=<smtp server>
# # smtp_username=<username>
# # smtp_password=<password>
# # email_recovery_sender=clearwater@example.org

# # Keys
# signup_key=secret
# turn_workaround=secret
# ellis_api_key=secret
# ellis_cookie_key=secret" | sudo tee /etc/clearwater/config;
# '

# ssh -t ubuntu64@10.129.2.116 'sudo touch /etc/clearwater/config;

# echo "
# # Deployment definitions
# home_domain=ims.hom
# sprout_hostname=sprout.ims.hom
# chronos_hostname=10.129.2.116:7253
# hs_hostname=hs.ims.hom:8888
# hs_provisioning_hostname=hs.ims.hom:8889
# ralf_hostname=ralf.ims.hom:10888
# xdms_hostname=homer.ims.hom:7888

# # Local IP configuration
# local_ip=10.129.2.116
# public_ip=10.129.2.116
# public_hostname=ellis

# # Email server configuration
# # smtp_smarthost=<smtp server>
# # smtp_username=<username>
# # smtp_password=<password>
# # email_recovery_sender=clearwater@example.org

# # Keys
# signup_key=secret
# turn_workaround=secret
# ellis_api_key=secret
# ellis_cookie_key=secret" | sudo tee /etc/clearwater/config;
# '

# Node specific installation instructions

# ssh -t ubuntu64@10.129.2.111 'sudo DEBIAN_FRONTEND=noninteractive apt-get install bono restund --yes'

# ssh -t ubuntu64@10.129.2.112 '
# sudo DEBIAN_FRONTEND=noninteractive apt-get install sprout --yes
# '

# ssh -t ubuntu64@10.129.2.118 '
# sudo DEBIAN_FRONTEND=noninteractive apt-get install clearwater-cassandra --yes
# sudo DEBIAN_FRONTEND=noninteractive apt-get install homestead homestead-prov --yes
# '

# ssh -t ubuntu64@10.129.2.114 '
# sudo DEBIAN_FRONTEND=noninteractive apt-get install clearwater-cassandra --yes
# sudo DEBIAN_FRONTEND=noninteractive apt-get install homer --yes
# '

# ssh -t ubuntu64@10.129.2.115 'sudo DEBIAN_FRONTEND=noninteractive apt-get install ralf --yes'

# ssh -t ubuntu64@10.129.2.116 'sudo DEBIAN_FRONTEND=noninteractive apt-get install ellis --yes'
