import scrapy
from scrapy.selector import Selector
from scrapy.http import Request


class ProductSpider(scrapy.Spider):
    name = 'product'
    allowed_domains = ['www.art-kozmetika.com']
    start_urls = ['http://www.art-kozmetika.com/']

    def parse(self, response):
        title = response.xpath("//div[3]/div/div[1]/h3/text()").get()
        nav_list = response.xpath('//*[@id="mainMenu"]/li').getall()
        a_hrefs = []
        for li in nav_list[0:4]:
            sel = Selector(text=li)
            selected_xpath = sel.xpath('//div/div/div/ul/li/a/@href').getall()
            a_hrefs.extend(selected_xpath)
        # a_hrefs = a_hrefs[:2]

        for a in a_hrefs:
            yield Request(a, callback=self.analyse_products, meta={"product": True})

    def analyse_products(self, response):
        product_urls = response.xpath('//*[@id="product-list-container"]/div/ul/li[1]/div/div[1]/a/@href').getall()
        for product_url in product_urls:
            yield Request(product_url, callback=self.analyse_product, meta={"product": True})

    def analyse_product(self, response):
        sku = response.xpath("//*[@id='product-addtocart-button']/@data-id").get()
        name = response.xpath('//*[@id="maincontent"]/div[1]/h1/text()').get()
        description = response.xpath("//*[@id='box-description']/div[2]/div//text()").getall()
        description = " ".join(description)
        short_description = response.xpath('//*[@id="product_addtocart_form"]/div[2]/div[2]/div[4]//text()').getall()
        short_description = " ".join(short_description)
        image_link = response.xpath('//*[@id="zoom-btn"]/@href').get()
        additional_links = response.xpath('//*[@id="itemslider-zoom"]/div[1]//a/@href').getall()
        availability = response.xpath('//*[@id="product_addtocart_form"]/div[2]/div[2]/ul/li/span[@class="in-stock"]//text()').get()
        qty = response.xpath('//*[@id="qty"]/@value').get()
        price = response.xpath('//*[@id="product_addtocart_form"]/div[2]/div[2]/div[3]/p[2]/span[2]/span[2]/text()').get()
        weights = response.xpath('//*[@id="box-description"]/div[2]/div/p[1]//text()').getall()
        weigth_val = ""
        for index, weight in enumerate(weights):
            if "kg" in weight:
                weigth_val = weights[index]
                break

        custom_option_name = response.xpath('//*[@id="product-options-wrapper"]/dl/div[1]/label/text()').get()
        type_of_options = response.xpath('//*[@id="product-options-wrapper"]/dl/div/div[@class="input-box"]/select').get()
        if type_of_options is None:
            custom_options = response.xpath('//*[@id="options-831-list"]/li/span/label//text()').getall()
        else:
            custom_options = response.xpath('//*[@id="select_877"]/option/text()').getall()

        other_options_names = response.xpath('//*[@id="product-options-wrapper"]/dl/div[2]/div//span/label/text()').getall()
        other_options_prices = response.xpath('//*[@id="product-options-wrapper"]/dl/div[2]/div//span/span[1]/text()').getall()



        yield {
            "sku": sku,
            "name": name,
            "description": description,
            "short_description" : short_description,
            "link" : response.request.url,
            "image_link":image_link,
            "additional_links":additional_links,
            "availability": availability,
            "Qty": qty,
            "price": price,
            "weight": weigth_val,
            "custom_option_name": custom_option_name,
            "custom_options": custom_options,
            'other_options_names' : other_options_names,
            'other_options_prices' : other_options_prices

        }


'''
 from scrapy import Selector
 li_list = response.xpath('//*[@id="mainMenu"]/li')
>>> sel = Selector(text=li_list[0])
>>> selected_xpath = sel.xpath('//div/div/div/ul/li/a')


'''
