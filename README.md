vcjobsearch
===========

Use Python and Scrapy to explore the portfolios of VC Firms.
Scrapes a company's name, url, location, description, and finds their careers webpage.


**How to Use:**  
1. Go to top-level directory  
2. Run 'scrapy crawl a16z > items.json' to output scraped data to json file  
3. Profit  


**Future Fixes:**
* Instead of crawling through one specific VC firm's portfolio, crawl through crunchbase's database
* Crunchbase has a well-defined, consistent structure to make scraping easier
* Potentially use crunchbase's provided api
