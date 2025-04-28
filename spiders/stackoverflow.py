import scrapy
from StackOverflow.items import StackoverflowItem, SoCommentItem
import logging
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('monitor')
logger.setLevel(logging.INFO)

fh = logging.FileHandler('monitor.log')
fh.setLevel(logging.INFO)

fh.setFormatter(formatter)
logger.addHandler(fh)

class StackoverflowSpider(scrapy.Spider):
    name = 'stackoverflow'
    allowed_domains = ['stackoverflow.com']
    # start_urls = ['http://stackoverflow.com/']

    def __init__(self):
        self.count = 1
    def start_requests(self):
        base_urls = "https://stackoverflow.com/questions/tagged/java?tab=votes&page={page}&pagesize=50"
        urls = [base_urls.format(page=page) for page in range(1, 51)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        for index in range(1, 51):
            self.count += 1
            if self.count % 100 == 0:
                logger.info(self.count)
            sel = response.xpath('//*[@id="questions"]/div[{index}]'.format(index=index))
            item = StackoverflowItem()
            item['votes'] = sel.xpath('./div[1]/div[1]/span[1]/text()').extract()
            # //*[@id="question-summary-11227809"]/div[1]/div[2]/span[1]

            item['answers'] = sel.xpath('./div[1]/div[2]/span[1]/text()').extract()
            # //*[@id="question-summary-11227809"]/div[1]/div[3]/span[1]

            item['views'] = sel.xpath('./div[1]/div[3]/span[1]/text()').extract()
            # //*[@id="question-summary-11227809"]/div[2]/h3/a

            item['questions'] = sel.xpath('./div[2]/h3/a/text()').extract()

            # //*[@id="question-summary-11227809"]/div[2]/h3/a

            item['links'] = "".join(sel.xpath('./div[2]/h3/a/@href').extract()).split("/")[2]
            # //*[@id="question-summary-11227809"]/div[2]/div[2]/div[1]/a[1]

            item['tags'] = ",".join(sel.xpath('./div[2]/div[2]/div[1]/a/text()').extract())
            yield item
            yield scrapy.Request(url="https://stackoverflow.com/questions/"+item['links']+"/"+item['questions'][0], callback=self.parse_next)

    def parse_next(self, response):
        # csel = response.xpath('//*[@id="content"]/div/div[1]')
        comment_list = response.xpath('//ul[@class="comments-list js-comments-list"]/li')
        item = SoCommentItem()
        for li in comment_list:
            item['question_header'] = response.xpath('//*[@id="question-header"]/h1/a/text()').extract()
            item['comments'] = ",".join(li.xpath('./div[2]/div/span[1]//text()').extract())
            if  len(li.xpath('./div[2]/div/div/a/text()')):
                item['comment_user'] = li.xpath('./div[2]/div/div/a/text()').extract()
            else:
                item['comment_user'] = [""]
            if len(li.xpath('//ul[@class="comments-list js-comments-list"]/li/div[2]/div/span[2]/a/span/text()')):
                item['comment_date'] = li.xpath('//ul[@class="comments-list js-comments-list"]/li/div[2]/div/span[2]/a/span/text()').extract()
            else:
                item['comment_date'] = [""]
            if  len(li.xpath('./div[1]/div/span/text()')):
                item['comment_vote'] = li.xpath('./div[1]/div/span/text()').extract()
            else:
                item['comment_vote'] = [""]
            yield item
        # yield item