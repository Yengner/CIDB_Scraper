# CIDB_Scraper
 Yengner Bermudez
 
 Web Scraping a contractor website based on malaysia.
 
 This web scraper uses selenium and goes through each link name "display" to collect the data that doesnt appear on the regular table such.
 
Data_collection.py
 I had trouble originial getting selenium to click on the link realizing
 that in the html the href was '#' meaning that this page was dynamically loaded was using javascript to load the iframe which made it significantly more difficult. 

 I ended up using universally unique identifier as i noticed after digging deeper into the html and network that a document is open and it adds a UUID to the original URL. I was able to extract the UUID from the display link.

 I had selenium apply 1000 to tthe drop down menu to display the 1000 contractors. I also applied expired try to get all the expired ones as well.
 I looped through all 1000 of the display links and grabbed each individual UUID number and put them inside a list called data_flags

 Scraper.py
 After importing the data from Data_collelection.py, i just clean up the data and iterate through all the urls using the data_flags. Selenium goes to each of these URLS and extracts the data from them. I then clean the data and push it onto an excel file. I also added a little animation that finishes when the code finishes as i put no header for selenium so it does not repetitivly open a new window everytime.
