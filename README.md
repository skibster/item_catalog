# Catalog App
Project 3: Item Catalog

1. This project runs a web application that allows a user to manage items in a catalog.
2. To install the virtual machine environment, you will install Git, Virtual Box and Vagrant. Detailed installation instructions can be found here: https://www.udacity.com/wiki/ud197/install-vagrant
3. Download this item_catalog repository using git@github.com:skibster/item_catalog.git
4. In your terminal, run the following commands:  
  * cd /path/to/item_catalog (changes directories to the 'item_catalog' repository directory).  
  * vagrant up (starts the virtual machine). 
  * vagrant ssh (creates a remote connection to your virtual machine).  
  * cd /vagrant/item_catalog  (changes directories to the 'item_catalog' directory in your virtual machine).  
  * python catalog_database_setup.py (this generates the database needed for the web application).
  * python catalog_seed_data.py (this command seeds the database with the categories that appear in the application).
  * python item_catalog.py (this begins the web application http server).
 5. Launch your browser and navigate to the URL: localhost:8000/catalog

Results:
The Catalog app should be running.

Features of Catalog App:
1. Users can browse the items in the categories.
2. Logged in users who authenticate using oAuth with Google Plus are able to add, edit and delete items to the Categories, including uploading images. As users add, edit and delete their entries, they are protected against Cross Site Forgery attacks.
3. API endpoints are available in both JSON and XML.
  * For a JSON response, call the URL: http://localhost:8000/catalog/json
  * For an XML response, call the URL: http://localhost:8000/catalog/xml
