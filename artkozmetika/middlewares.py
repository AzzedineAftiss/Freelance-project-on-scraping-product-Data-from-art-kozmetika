# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from scrapy import signals
from selenium.webdriver.support.ui import WebDriverWait

import logging

class ArtkozmetikaSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ArtkozmetikaDownloaderMiddleware:


    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-gpu")
        desired_capabilities = options.to_capabilities()
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=desired_capabilities ) # , desired_capabilities=desired_capabilities,
        # self.service = Service(executable_path=ChromeDriverManager().install())
        # self.driver = webdriver.Chrome(service=self.service)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        # crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        # crawler.signals.connect(s.spider_closed, signals.spider_closed)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):


        print(f"request url : {request.url}")
        logging.info("azzedine azzedine")
        self.driver.get(request.url)
        # self.driver.get("https://www.youtube.com/watch?v=hi_uVfBFbTI")
        # WebDriverWait(self.driver, 10).until(
        #     EC.element_to_be_clickable((By.CLASS_NAME, '_3t7zg'))
        # )
        body = str.encode(self.driver.page_source)
        time.sleep(20)
        # Expose the driver via the "meta" attribute
        request.meta.update({'driver': self.driver})
        self.driver.implicitly_wait(15)
        return HtmlResponse(
            self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self):
        """Shutdown the driver when spider is closed"""
        time.sleep(50)
        self.driver.quit()