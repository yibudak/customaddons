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
read -e -s -p "Enter the Database password: " DBPASS
echo -e "\n"
read -e -s -p "Enter the Odoo Administrator Password: " OE_SUPERADMIN
echo -e "\n"

OE_USER="odoo"
OE_HOME="/opt/$OE_USER/11"
OCA_HOME="/opt/odoo/11/repos"
OE_HOME_EXT="$OE_HOME/server"
OE_SERVERTYPE="server"
OE_VERSION="11.0"
OE_CONFIG="odoo-server11"

# Odoo user
echo -e "\n---- Enter odoo system users password and info ----"
sudo adduser odoo --home=/opt/$OE_USER

sudo apt update
sudo apt upgrade -y

apt-get install postgresql postgresql-contrib -y

sudo sed -i s/"#listen_addresses = 'localhost'"/"listen_addresses = '*'"/g /etc/postgresql/10/main/postgresql.conf

sudo systemctl enable postgresql

echo -e "\n---- Enter password for ODOO PostgreSQL User  ----"
sudo su - postgres -c "createuser --createdb --username postgres $OE_USER"
# sudo su - postgres -c 'ALTER USER $OE_USER WITH SUPERUSER;'
echo -e "\n---- Creating postgres unaccent search extension  ----"
sudo su - postgres -c 'psql template1 -c "CREATE EXTENSION \"unaccent\"";'

sudo -u postgres psql -U postgres -d postgres -c "alter user $OE_USER with password '$DBPASS';"



sudo apt-get install git python3 python3-pip python3-suds python3-all-dev \
python3-dev python3-setuptools python3-tk -y

sudo apt install git libxml2-dev libxslt1-dev libevent-dev libsasl2-dev libldap2-dev \
pkg-config libtiff5-dev libjpeg8-dev libjpeg-dev zlib1g-dev libfreetype6-dev \
liblcms2-dev liblcms2-utils libwebp-dev tcl8.6-dev tk8.6-dev libyaml-dev fontconfig -y

sudo -H pip3 install --upgrade pip

sudo apt install npm  -y
sudo npm install -g less

sudo -H pip3 install -r ./requirements.txt

tar vxf wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
sudo cp wkhtmltox/bin/wk* /usr/local/bin/
wkhtmltopdf --version


echo -e "\n---- Create Log directory ----"
sudo mkdir /var/log/$OE_USER
sudo chown $OE_USER:$OE_USER /var/log/$OE_USER

#--------------------------------------------------
# Install ODOO
#--------------------------------------------------

echo -e "\n---- Create directories ----"
sudo su $OE_USER -c "mkdir -p $OE_HOME"
sudo su $OE_USER -c "mkdir -p $OCA_HOME"
sudo su $OE_USER -c "mkdir -p $OE_HOME/addons"
sudo su $OE_USER -c "mkdir -p $OE_HOME/data"
sudo su $OE_USER -c "mkdir -p $OE_HOME_EXT"

echo -e "\n==== Installing ODOO Server ===="
sudo su $OE_USER -c "git clone  --depth 1 --branch $OE_VERSION https://github.com/aaltinisik/OCBAltinkaya.git $OE_HOME_EXT/"

echo -e "\n---- Setting permissions on home folder ----"
sudo chown -R $OE_USER:$OE_USER $OE_HOME/*

echo -e "* Create server config file"

sudo rm /etc/$OE_CONFIG.conf
sudo touch /etc/$OE_CONFIG.conf
sudo chown $OE_USER:$OE_USER /etc/$OE_CONFIG.conf
sudo chmod 640 /etc/$OE_CONFIG.conf

echo -e "* Change server config file"

sudo su root -c "echo '[options]' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'db_host = localhost' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'db_user = $OE_USER' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'db_port = False' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'db_password = $DBPASS' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'admin_passwd = $OE_SUPERADMIN' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'addons_path = $OE_HOME_EXT/addons,$OE_HOME/addons,$OCA_HOME/customaddons' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '## Server startup config - Common options' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# Admin password for creating, restoring and backing up databases admin_passwd = admin' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify additional addons paths (separated by commas)' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '## XML-RPC / HTTP - XML-RPC Configuration' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'unaccent = True' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'xmlrpc = True' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# Specify the TCP IP address for the XML-RPC protocol. The empty string binds to all interfaces.' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'xmlrpc_interface  = ' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify the TCP port for the XML-RPC protocol' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'xmlrpc_port = 8069' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# Enable correct behavior when behind a reverse proxy' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'proxy_mode = False' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '## XML-RPC / HTTPS - XML-RPC Secure Configuration' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# disable the XML-RPC Secure protocol' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'xmlrpcs = True' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# Specify the TCP IP address for the XML-RPC Secure protocol. The empty string binds to all interfaces.' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'xmlrpcs_interface = ' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify the TCP port for the XML-RPC Secure protocol' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'xmlrpcs_port = 8071' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify the certificate file for the SSL connection' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'secure_cert_file = server.cert' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify the private key file for the SSL connection' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'secure_pkey_file = server.pkey' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '## NET-RPC - NET-RPC Configuration' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# enable the NETRPC protocol' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'netrpc = False' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify the TCP IP address for the NETRPC protocol' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'netrpc_interface = 127.0.0.1' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify the TCP port for the NETRPC protocol' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'netrpc_port = 8070' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '## WEB - Web interface Configuration' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# Filter listed database REGEXP' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'dbfilter = .*' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '## Static HTTP - Static HTTP service' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# enable static HTTP service for serving plain HTML files' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'static_http_enable = False' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify the directory containing your static HTML files (e.g '/var/www/')' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'static_http_document_root = None' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify the URL root prefix where you want web browsers to access your static HTML files (e.g '/')' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'static_http_url_prefix = None' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '## Testing Group - Testing Configuration' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# Launch a YML test file.' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'test_file = False' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# If set, will save sample of all reports in this directory.' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'test_report_directory = False' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# Enable YAML and unit tests.' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '## Server startup config - Common options' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'test_disable = False' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# Commit database changes performed by YAML or XML tests.' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'test_commit = False' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '## Logging Group - Logging Configuration' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# file where the server log will be stored (default = None)' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'logfile = /var/log/$OE_USER/$OE_CONFIG$1.log' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# do not rotate the logfile' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'logrotate = True' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# Send the log to the syslog server' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'syslog = False' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# setup a handler at LEVEL for a given PREFIX. An empty PREFIX indicates the root logger. This option can be repeated. Example: "openerp.orm:DEBUG" or "werkzeug:CRITICAL" (default: ":INFO")' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'log_handler = ["[':INFO']"]' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify the level of the logging. Accepted values: info, debug_rpc, warn, test, critical, debug_sql, error, debug, debug_rpc_answer, notset' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '#log_level = debug' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'log_level = info' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'data_dir = $OE_HOME/data' >> /etc/$OE_CONFIG.conf"



#--------------------------------------------------
# Adding ODOO as a deamon (initscript)
#--------------------------------------------------
echo -e "* SystemD Init File"

sudo rm /etc/systemd/system/odoo11.service
sudo touch /etc/systemd/system/odoo11.service
sudo chown root: /etc/systemd/system/odoo11.service
sudo chmod 755 /etc/systemd/system/odoo11.service

sudo su root -c "echo '[Unit]' >> /etc/systemd/system/odoo11.service"
sudo su root -c "echo 'Description=Odoo Open Source ERP and CRM' >> /etc/systemd/system/odoo11.service"
sudo su root -c "echo 'After=network.target' >> /etc/systemd/system/odoo11.service"
sudo su root -c "echo '[Service]' >> /etc/systemd/system/odoo11.service"
sudo su root -c "echo 'Type=simple' >> /etc/systemd/system/odoo11.service"
sudo su root -c "echo 'User=odoo' >> /etc/systemd/system/odoo11.service"
sudo su root -c "echo 'Group=odoo' >> /etc/systemd/system/odoo11.service"
sudo su root -c "echo 'ExecStart=$OE_HOME_EXT/odoo-bin --config /etc/$OE_CONFIG.conf' >> /etc/systemd/system/odoo11.service"
sudo su root -c "echo 'KillMode=mixed' >> /etc/systemd/system/odoo11.service"
sudo su root -c "echo '[Install]' >> /etc/systemd/system/odoo11.service"
sudo su root -c "echo 'WantedBy=multi-user.target' >> /etc/systemd/system/odoo11.service"


sudo systemctl enable odoo11.service
sudo systemctl start odoo11.service


echo -e "* Open ports in UFW for openerp-server"
sudo ufw allow 8069

./install-customaddons.sh
