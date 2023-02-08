#!/bin/bash                                                                                                                                                                                                  

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT

iptables -A INPUT -p tcp --dport 22 -s 10.0.1.2 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -s 10.0.3.3 -j ACCEPT
iptables -A INPUT -p tcp --sport 22 -s 10.0.3.0/24 -j ACCEPT

iptables -A INPUT -p tcp --dport 5000 -i eth0 -s 10.0.1.2 -j ACCEPT
iptables -A INPUT -p tcp --sport 5000 -i eth0 -s 10.0.2.4 -j ACCEPT
iptables -A INPUT -p tcp --sport 5000 -i eth0 -s 10.0.2.3 -j ACCEPT       

iptables -A INPUT -p tcp --dport 80 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp --sport 80 -m state --state ESTABLISHED,RELATED -j ACCEPT

iptables -A INPUT -p tcp --sport 443 -i eth0 -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT

iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A INPUT -p udp --sport 53 -j ACCEPT

ip route del default
ip route add default via 10.0.1.2 dev eth0

service ssh start
service rsyslog start

echo "10.0.1.4   myserver.local" >> /etc/hosts
echo "10.0.2.3	auth.local" >> /etc/hosts
echo "10.0.2.4	file.local" >> /etc/hosts 

python3 broker.py

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi



