#!/bin/bash
# -*- encoding: utf-8 -*-

# To run with ubuntu 18.04
#wget https://raw.githubusercontent.com/aaltinisik/customaddons/11.0/install-odoo11.sh
#chmod +x install-odoo.sh
#./install-odoo.sh


#--------------------------------------------------
# Set Locale en_US.UTF-8
#--------------------------------------------------
echo -e "\n---- Set en_US.UTF-8 Locale ----"
sudo cp /etc/default/locale /etc/default/locale.BACKUP
sudo rm -rf /etc/default/locale
echo -e "* Change server config file"
sudo su root -c "echo 'LC_ALL="en_US.UTF-8"' >> /etc/default/locale"
sudo su root -c "echo 'LANG="en_US.UTF-8"' >> /etc/default/locale"
sudo su root -c "echo 'LANGUAGE="en_US:en"' >> /etc/default/locale"
export LC_ALL=C



echo 'Acquire::ForceIPv4 "true";' | tee /etc/apt/apt.conf.d/99force-ipv4
touch /etc/sysctl.d/disableipv6.conf
echo "net.ipv6.conf.all.disable_ipv6=1" >> /etc/sysctl.d/disableipv6.conf


echo -e "---- Decide system passwords ----"
read -e -s -p "Enter odoo system users password: " OE_USERPASS
echo -e "\n"
read -e -s -p "Enter the Database password: " DBPASS
echo -e "\n"
read -e -s -p "Enter the Odoo Administrator Password: " OE_SUPERADMIN
echo -e "\n"



OE_USER="odoo"
OE_HOME="/opt/$OE_USER/odoo11"
OCA_HOME="/opt/odoo/odoo11/repos"
OE_HOME_EXT="$OE_HOME/$OE_USER-server"
OE_SERVERTYPE="openerp-server"
OE_VERSION="11.0"
OE_CONFIG="odoo-server11"

# Odoo user
echo -e "\n---- Enter odoo system users info ----"
sudo adduser odoo --home=/opt/$OE_USER

sudo apt update
sudo apt upgrade -y


sudo apt-get install git python3 python3-pip python3-suds python3-all-dev \
python3-dev python3-setuptools python3-tk -y

sudo apt install git libxml2-dev libxslt1-dev libevent-dev libsasl2-dev libldap2-dev \
pkg-config libtiff5-dev libjpeg8-dev libjpeg-dev zlib1g-dev libfreetype6-dev \
liblcms2-dev liblcms2-utils libwebp-dev tcl8.6-dev tk8.6-dev libyaml-dev fontconfig -y

sudo -H pip3 install --upgrade pip

sudo apt install npm  -y
sudo npm install -g less


sudo -H pip3 install -r /opt/odoo/doc/requirements.txt
sudo -H pip3 install -r /opt/odoo/requirements.txt

sudo curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash - \
&& sudo apt-get install -y nodejs \
&& sudo npm install -g less less-plugin-clean-css

