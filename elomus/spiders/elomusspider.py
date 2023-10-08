from urllib.parse import urljoin

import scrapy


class ElomusspiderSpider(scrapy.Spider):
    name = "elomusspider"
    allowed_domains = ["elomus-theme.myshopify.com"]
    start_urls = ["https://elomus-theme.myshopify.com/collections"]

    def parse(self, response):
        shop_categories = response.css(".col-md-4 a::attr(href)").getall()
        for category in shop_categories:
            detailed_url = urljoin(response.url, category)
            yield scrapy.Request(
                detailed_url, callback=self.parse_category
            )


    def parse_category(self, response):
        product_links = response.css(
            ".product-layout .item-inner a:not([href*='javascript:void(0);'])::attr(href)").getall()
        for link in product_links:
            detailed_url = urljoin(response.url, link)
            yield scrapy.Request(
                detailed_url, callback=self.parse_product
            )


    def parse_product(self, response):
        title = response.css("h2.product-name::text").get()
        tags = response.css(".short-des a::text").getall()
        vendor = response.css("li:contains('Brand') a::text").get()
        options = response.css(
            ".swatch[data-option-index='0'] [data-value]::attr(data-value)"
        ).getall()
        yield {
            "title": title,
            "tags": tags,
            "vendor": vendor,
            "options": options,
        }