import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Connect to the router
ssh.connect("192.168.88.1", username="admin", password="password")
# Set the DHCP server to only respond with the router for a DNS server (change 0 to the DHCP server you want to modify)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/ip dhcp-server network set 0 dns-server=192.168.88.1")
# Redirect all other DNS requests to the router to help mitigate manual DNS changes (optional)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/ip firewall nat add chain=dstnat dst-port=53 action=redirect to-ports=53 protocol=tcp")
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/ip firewall nat add chain=dstnat dst-port=53 action=redirect to-ports=53 protocol=udp")
# parse domains
with open('domains.txt') as f:
    lines = [line.rstrip() for line in f]
# add the static DNS, in this case it returns 127.0.0.1 but it can be changed to return any IP
for domain in lines:
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/ip dns static add name=" + domain + " address=127.0.0.1")
ssh.close();