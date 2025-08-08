# Encircle Marketing Technical Test
These scrapers require the modules present at the top of each python file. All code was written using the python IDLE and run in python IDLE Shell 3.11.2.
  
They will attempt to iterate through each of the three 3-part tyre inputs provided in the technical test document and will skip one if the websites they are scraping can not find any results. This should allow for erroneous data entry not to disrupt a lengthy scraping run.
  
The third website (https://www.bythjul.com/) is in Swedish and while the robots.txt file does not explicitly ban scraping the tyre section of the website, they have cloudflare anti bot measures in place. It is possible they still allow scraping however as I do not know Swedish I am unable to check this in their terms and conditions. Therefore, the scraping of bythjul.com was not attempted.
  
The two websites that were scraped therefore were:  
www.dexel.co.uk  
https://www.national.co.uk  
  
Pandas was used to create the database with the following structure: 
"Site", "Store", "Brand", "Pattern","Size","Type","Price"
  
Where:  
Site - the website scraped  
Store - for dexel specific stores could be selected, in its current state the script will select the first store for stock however if `check_all_stores` is updated to True it will look through all other stores and distinguish any consequent data scraped by specifying the store it scraped from  
Brand - brand of tire, this is taken from the alt text for the logos used in product listings  
Pattern - tyre pattern  
Size - tyre size  
Price - price of tyre as reported by the sites scraped  
