apt-get -qqy update
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-flask python-sqlalchemy
apt-get -qqy install python-pip
pip install bleach
pip install oauth2client
pip install requests
pip install httplib2
pip install WTForms

vagrantTip="The shared directory is located at /vagrant\nTo access your shared files: cd /vagrant"
echo -e $vagrantTip > /etc/motd

