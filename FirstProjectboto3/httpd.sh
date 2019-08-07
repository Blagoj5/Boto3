#!/bin/bash
apt-get update -y
apt-get upgrade -y
apt-get install apache2 -y && service apache2 start
cd /var/www/html
echo "<html><h1>It's properly working !!!!! </h1></html>" >> index.html
echo "template is working and public ip is $Variables" >> testing.html
cd ~
echo "It's working $USER" > test.txt
