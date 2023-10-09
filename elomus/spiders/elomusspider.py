from urllib.parse import urljoin, urlparse
import json
import scrapy


class ElomusspiderSpider(scrapy.Spider):
    name = "elomusspider"
    allowed_domains = ["elomus-theme.myshopify.com"]
    start_urls = ["https://elomus-theme.myshopify.com/collections"]

    # main method for parsing all data
    def parse(self, response):
        shop_categories = response.css(".col-md-4 a::attr(href)").getall()
        for category in shop_categories:
            detailed_url = urljoin(response.url, category)
            yield scrapy.Request(
                detailed_url, callback=self.parse_category
            )


    # method to parse specific category
    def parse_category(self, response):
        # getting product_type if json creating is no available
        category_path = urlparse(response.url).path
        path_parts = category_path.split('/')
        product_type = path_parts[-1]

        # product_links = response.css(
        #     ".product-layout .item-inner a:not([href*='javascript:void(0);'])::attr(href)").getall()

        # getting links for all products on the page
        product_links = response.css(
            ".images-container > a::attr(href)"
        ).getall()

        for link in product_links:
            detailed_url = urljoin(response.url, link)

            #getting json data
            product_info = response.css(
                f"a[href='{link}'] + .button-group .quickview::attr(data-productinfo)").get()

            yield scrapy.Request(
                detailed_url,
                callback=self.parse_product,
                meta={
                    "product_type": product_type,
                    "product_info": product_info,
                }
            )

        # scrape all pages if it is
        next_page = response.css(
            'li.pagination-next a::attr(href)').get()
        if next_page is not None:
            next_page_url = urljoin(response.url, next_page)
            yield scrapy.Request(next_page_url, callback=self.parse_category)


    def parse_product(self, response):

        #if json file is not available
        created_at = None
        published_at = None
        updated_at = None

        title = response.css("h2.product-name::text").get()
        body_html = response.css('body').get()
        options = response.css(
            ".swatch[data-option-index='0'] [data-value]::attr(data-value)"
        ).getall()
        product_type = response.meta.get('product_type')
        tags = response.css(
            'p.short-des a::text'
        ).getall()
        vendor = response.css(
            'ul.list-unstyled li:nth-child(1) a::text'
        ).get()
        id_num = response.css("input#product-identify::attr(value)").get()
        images = response.css(
            ".sub-image > .lazyload::attr(data-src)"
        ).getall()
        variants = None

        # if json is available
        if response.meta.get('product_info') is not None:
            product_info = json.loads(response.meta.get('product_info'))

            created_at = product_info.get('created_at')
            published_at = product_info.get('published_at')
            try:
                updated_at = product_info.get("variants")[0].get('featured_image').get('updated_at')
            except AttributeError:
                updated_at = None
            tags = product_info.get('tags')
            vendor = product_info.get('vendor')
            product_type = product_info.get('type')
            images = product_info.get('images')
            id_num = product_info.get('id')
            variants = [variant["id"] for variant in product_info.get('variants')]

        yield {
            "id": id_num,
            "title": title,
            "body_html": body_html,
            "published_at": published_at,
            "created_at": created_at,
            "updated_at": updated_at,
            "vendor": vendor,
            "product_type": product_type,
            "tags": tags,
            "variants": variants,
            "images": images,
            "options": options,
        }