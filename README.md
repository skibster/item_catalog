# Catalog App
Project 3: Item Catalog

1. This project runs a Flask web application that allows users to manage items in a catalog.
2. To install the virtual machine environment, you will install Git, Virtual Box and Vagrant. Detailed installation instructions can be found here: https://www.udacity.com/wiki/ud197/install-vagrant
3. Download this item_catalog repository using `git close git@github.com:skibster/item_catalog.git`
4. In your terminal, run the following commands:  
  * `cd /path/to/item_catalog` (changes directories to the 'item_catalog' repository directory).  
  * `vagrant up` (starts the virtual machine). 
  * `vagrant ssh` (creates a remote connection to your virtual machine).  
  * `cd /vagrant/item_catalog` (this changes directories to the 'item_catalog' directory in your virtual machine).  
  * `python catalog_database_setup.py` (this generates the database needed for the web application).
  * `python catalog_seed_data.py` (this command seeds the database with the categories that appear in the application. If more categories are desired, you can edit the `names` variable in this file before running it).
  * `python item_catalog.py` (this begins the web application's HTTP server). Press Ctrl-C to interrupt and halt the HTTP server.
 5. Launch your browser and navigate to the URL: http://localhost:8000/catalog

Results:
The Catalog app should be up and running.

Features of Catalog App:
1. Users can browse the items in the categories. Initially, there will not be items until users add them.
2. Logged in users can authenticate using Google Plus' oAuth API. Once authenticated, users are able to add items (including images), edit and delete items to the Categories. As users add, edit and delete their entries, the web application is built to protected them against Cross-Site Request Forgery (CSRF) attacks.
3. In addition to the web browser user interface, several API endpoints are available in both JSON and XML to retrieve the contents of the catalog.
  * For a JSON response, make a GET request to URL: http://localhost:8000/catalog/json
  * For an XML response, make a GET request to URL: http://localhost:8000/catalog/xml
