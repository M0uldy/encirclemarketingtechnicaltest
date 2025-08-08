# Encircle Marketing Technical Test
These scrapers require the modules present at the top of each python file.

They will attempt to iterate through each of the three 3-part tyre inputs provided in the technical test document and will skip one if the websites they are scraping can not find any results. This should allow for erroneous data entry not to disrupt a lengthy scraping run.

The third website (https://www.bythjul.com/) is in Swedish and while the robots.txt file does not explicitly ban scraping the tyre section of the website, they have cloudflare anti bot measures in place. It is possible they still allow scraping however as I do not know Swedish I am unable to check this in their terms and conditions. Therefore, the scraping of bythjul.com was not attempted.
