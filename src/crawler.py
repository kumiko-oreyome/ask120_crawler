from requests_html import AsyncHTMLSession
from .webparser import parse_single_question_page,QuestionListPage
from .item import QuestionItem,AnswerItem,QAItem
from lxml import etree,html
from urllib.parse import urljoin

urls = ['http://www.120ask.com/question/49585155.htm','http://www.120ask.com/question/59160474.htm'\
           ,'http://www.120ask.com/question/71754746.htm','http://www.120ask.com/question/41833757.htm']


#results = asession.run(*requests)
#print(results)




class Ask123Crawler():
    #TODO default backend is text file backend
    def __init__(self,driver,backend=None):
        self.asession = AsyncHTMLSession()
        self.driver =  driver 
        self.backend = backend
        
    def crawl_single_question_page(self,url,qid):
        async def foo():
            r = await self.asession.get(url)
            title,description,answers =  parse_single_question_page(r.content)
            q = QuestionItem(qid,title,description)
            al = [AnswerItem(content=d['answer'],time=d['time'],job=d['job']) for d in answers]
            qa_item = QAItem(q,al)
            if not self.backend.check_question_duplicate(qid):
                self.backend.save_qa_instance(qa_item)
            else:
                print('duplicate question %s %s'%(qid,title))
            print('successfully parse %s'%(title))
        return foo

    def crawl_by_keywords(self,keywords):
        for keyword in keywords:
            start_url ='http://so.120ask.com/?kw=%s'%(keyword)
            current_url = start_url
            while True:
                links,ids,next_link = self.crawl_question_list_page(current_url)
                if next_link is None:
                    break
                if len(links) > 0: #有的時候會有一整頁都沒有可以用的連結的情況...
                    self.asession.run(*[ self.crawl_single_question_page(link,qid) for link,qid in zip(links,ids)])
                current_url = urljoin(start_url,next_link)

    def crawl_question_list_page(self,url):
        self.driver.implicitly_wait(15)
        self.driver.get(url)
        parser = QuestionListPage(self.driver.page_source)

        #有的時候第一時間沒有辦法渲染全部就直接parse了 然後就出錯 所以要check
        if not parser.check_page_ready():
            print('request again : %s'%(url))
            return self.crawl_question_list_page(url)
        result = list(parser.get_question_infos())
        links,ids = [],[]
        if len(result)>0:
            links,ids = zip(*result)
        next_link = parser.get_next_page_link()
        print(next_link)
        if next_link is not None:
            next_link = next_link[0]
        return links,ids,next_link




    #backend.collection.drop()

    #def crawl_by_keywords(self,keywords):
    #    pass 