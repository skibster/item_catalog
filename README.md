# Catalog App
Project 3: Item Catalog

1. This project runs a web application that allows a user to manage items in a catalog.
2. To install the virtual machine environment, you will install Git, Virtual Box and Vagrant. Detailed installation instructions can be found here: https://www.udacity.com/wiki/ud197/install-vagrant
3. Download this item_catalog repository.
4. In your terminal, run the following commands:  
  * cd /path/to/item_catalog (changes directories to the 'item_catalog' repository directory).  
  * vagrant up (starts the virtual machine). 
  * vagrant ssh (creates a remote connection to your virtual machine).  
  * cd /vagrant/item_catalog  (changes directories to the 'item_catalog' directory in your virtual machine).  
  * python catalog_database_setup.py (this generates the database needed for the web application).
  * python catalog_seed_data.py (this command seeds the database with the categories that appear in the application).
  * python item_catalog.py (this begins the web application http server).
 5. In your browser, go to localhost:8000

Results:
The Catalog app should be running.

Features of Catalog App:
0. Users can browse the items in the categories.
1. Logged in users who authenticate using oAuth with Google Plus also have the following features:
