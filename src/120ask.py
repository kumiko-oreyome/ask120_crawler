import scrapy
#from scrapy_splash import SplashRequest
import logging
from ..items import QAItem
from selenium import webdriver

class Ask120Spider(scrapy.Spider):
    name = "ask120"
    start_urls = ['http://so.120ask.com/?kw=123']


    def start_requests(self):
        #self.driver = webdriver.Chrome('./chromedriver.exe')
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse,
                                args={'wait':5,'timeout':10}, endpoint='render.html')


    def parse(self, response):
        #for item in self.parse_page(response):
        #    yield item
        # next page
        link = response.xpath("//div[@class='p_pagediv']//a[@title='下一页']/@href").extract_first(default=None)
        print('link')
        print(link)
        if link is not None:
            next_page = response.urljoin(link)
            yield scrapy.Request(url=next_page, callback=self.parse,
                              args={'wait':20,'timeout':30}, endpoint='render.html')
        else:
            with open('aa.html','w',encoding='utf-8') as f:
                print(response.text,file=f)
            print(response.xpath("//div[@class='p_pagediv']//a[@title='下一页']").extract())
            print('hasaki')
  
    def parse_page(self,response):
        for node in response.xpath("//div[@class='result_box']//ul//li"):
            title = node.xpath("string(.//h3/a)").extract_first()
            link = node.xpath("./span/text()").extract_first()
            if self.valid_question_link(link):
                detail_page = response.urljoin(link)
                yield scrapy.Request(detail_page, callback=self.parse_qa_detail,meta={'title':title,'link':detail_page})

    def parse_qa_detail(self,response):
        title = response.meta['title']
        link = response.meta['link']
        answer  = 'None'
        rl =  response.xpath("//div[@class='b_answerli']//div[@class='crazy_new']/p")
        if len(rl) > 0:
            answer = rl[0].xpath('string(.)').extract_first().strip()
        #print('- - - - '*30)
        #print('title : %s'%(title))
        #print('answer\n %s'%(answer))
        return QAItem(title=title,link=link,answer=answer)     


    def _next_page(self,response):
        link = response.xpath("//div[@class='p_pagediv']//a[@title='下一页']/@href").extract_first(default=None)
        #self.logger.info('wwwwwww'*100)

        if link is not None:
            self.logger.info('link --> %s'%(link))
            next_page = response.urljoin(link)
            yield SplashRequest(url=next_page, callback=self.parse,
                                args={'wait':5,'timeout':20}, endpoint='render.html')
        else:
            with open('aa.html','w',encoding='utf-8') as f:
                print(response.text,file=f)
                print('hasaki2')
            print('hasaki')
            yield None
           

       
    
    def valid_question_link(self,url):
        if url.startswith("http://www.120ask.com/question"):
            return True
        return False