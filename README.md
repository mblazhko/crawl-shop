# crawl-shop

The project made to scrape products from the e-commerce website https://elomus-theme.myshopify.com/.
For scraping was used Scrapy framework.

After scrapping you will get next data:
- id - unique id of the product
- title - name of the product
- body_html - html code of body tag
- published_at - date of publication
- created_at - date of creation
- updated_at - date of update if the product was updated
- vendor - the brand of the product
- product_type - the type of the product
- tags - tags of the product
- variants - id of product variants
- images - the product images urls
- options - options of the product like capacity, high, color etc.

## How to run
1. ```git clone https://github.com/mblazhko/crawl-shop.git```
2. Create a virtual environment:
   ```python -m venv env```
3. Activate the virtual environment:
   - For Windows:
   ``` .\env\Scripts\activate```
   - For macOS and Linux:
   ```source env/bin/activate```

4. Install the project dependencies:
   ```pip install -r requirements.txt```
5. Run the spider:
   ```
   scrapy crawl elomusspider -O elomus_data.csv
   ```
6. You will find data in the elomus_data.csv file.
