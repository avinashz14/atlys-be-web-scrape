import scrapy
import ipdb

from src.scraping.data_manager.product_data_manager import ProductDataManager
from src.scraping.data_manager.tasks_data_manager import TaskDataManager
from src.scraping.models import Product

from src.libs.utils import generate_unique_id
from scrapy.exceptions import CloseSpider
from scrapy.utils.response import response_status_message


class ProductSpider(scrapy.Spider):
    cnt = 0

    name = 'product-spider'
    scrapped_data = []
    custom_settings = {
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429],
        'DOWNLOAD_DELAY': 2,  # 2 seconds delay between retries
    }

    def __init__(self, url=None, task_id=None, proxy=None, *args, **kwargs):
        super(ProductSpider, self).__init__(*args, **kwargs)
        # self.page = int(kwargs.get('page', 1))
        self.limit = int(kwargs.get('limit', 1))
        self.task_id = task_id
        url = url.split("?")
        query_params = "" if len(url) < 2 else url[1]
        self.start_urls = ["{url}/page/{page}/?{query_params}".format(url=url[0], page=i + 1, query_params=query_params)
                           for
                           i in range(self.limit)]
        self.proxy = proxy

    def start_requests(self):
        # ipdb.set_trace()
        for url in self.start_urls:
            print(url)
            if self.proxy:
                yield scrapy.Request(url, callback=self.parse, meta={'proxy': self.proxy})
            else:
                yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        print(f"Scraped data from {response.url}")
        self.cnt += 1

        if response.status in self.custom_settings['RETRY_HTTP_CODES']:
            print(f"Retrying {response.url} (status: {response.status})")
            return self._retry(response.request, reason=response_status_message(response.status))

        product_list = []
        for product in response.css('li.col-xs-6.col-sm-4.col-md-3.col-lg-3.un-4-cols.product'):
            title = product.css('.mf-product-content h2.woo-loop-product__title a::text').get()
            image_url = product.css('.mf-product-thumbnail img::attr(data-lazy-src)').get()
            image_url_set = product.css('.mf-product-thumbnail img::attr(srcset)').get()
            price = product.css(
                '.mf-product-price-box .price ins .woocommerce-Price-amount BDI::text').get() or product.css(
                '.mf-product-price-box .price .woocommerce-Price-amount BDI::text').get()
            original_price = product.css(
                '.mf-product-price-box .price del .woocommerce-Price-amount BDI::text').get() or product.css(
                '.mf-product-price-box .price .woocommerce-Price-amount BDI::text').get()
            description = product.css(
                '.mf-product-content .woocommerce-product-details__short-description p::text').get(),

            d = {
                'title': title,
                'image_url': image_url,
                'image_url_set': image_url_set,
                'price': float(price) if isinstance(price, (str, float, int)) else None,
                'original_price': float(original_price) if isinstance(original_price, (str, float, int)) else None,
                'description': description,
            }
            product_list.append(d)

        self.scrapped_data += product_list

        product_data_ctl = ProductDataManager()
        product_data_ctl.load_product()
        updated_item_count = 0
        new_item_count = 0
        for data in self.scrapped_data:
            product = Product(
                title=data.get("title"),
                image_url=data.get("image_url"),
                price=data.get("price"),
                original_price=data.get("original_price"),
                id=generate_unique_id(data.get("title")),
            )

            success = product_data_ctl.save_product(product)
            updated_item_count += (1 if success == 2 else 0)
            new_item_count += (1 if success == 1 else 0)

        stats = {
            "total_scrapped_product": len(self.scrapped_data),
            "total_new_product": new_item_count,
            "total_updated_product": updated_item_count,
            # "total_failed_product": updated_item_count,
        }
        task_data = {
            "meta_data": stats,
            "status": "COMPLETE"
        }
        task_data_ctl = TaskDataManager()
        task_data_ctl.update_task_by_id(self.task_id, task_data)

    def _retry(self, request, reason):
        retries = request.meta.get('retry_times', 0) + 1
        if retries <= self.custom_settings['RETRY_TIMES']:
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            print(f"Retrying {retryreq.url} (retry {retries}/{self.custom_settings['RETRY_TIMES']})")
            return retryreq
        else:
            print(f"Giving up on {request.url} after {retries} retries")
            raise CloseSpider(f"Giving up on {request.url} after {retries} retries")
