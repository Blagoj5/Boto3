#!/bin/bash
yum update -y
yum upgrade -y
yum install httpd -y && service httpd start
yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm
sudo systemctl enable amazon-ssm-agent \
&& sudo systemctl start amazon-ssm-agent
mkdir ~/.aws \
&& echo -e "[default] \nregion = us-east-1" > ~/.aws/config 
cd /var/www/html
echo "<html><h1>It's properly working !!!!! </h1></html>" >> index.html
echo "template is working and public ip is $Variables" >> testing.html
cd ~
echo "It's working $USER" > test.txt
echo "*/15 * * * * root systemctl restart amazon-ssm-agent.service" >> /etc/crontab
