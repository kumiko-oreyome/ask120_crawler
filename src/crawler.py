from .page import HealthQuestionPage
from .item import QuestionItem,AnswerItem,QAItem
from lxml import etree,html

urls = ['http://www.120ask.com/question/49585155.htm','http://www.120ask.com/question/59160474.htm'\
           ,'http://www.120ask.com/question/71754746.htm','http://www.120ask.com/question/41833757.htm']



class KeywordQueryRequest():
    def __init__(self,driver):
        self.driver = driver
        self.MAX_TIME_RETRY = 20
        self.retry_cnt = 0
    def send(self,url):
        print('send')
        print('- '*49)
        try:
            self.driver.get(url)
        except:
            print('fuck %s'%(url))
            return  self.send(url)
        #有的時候第一時間沒有辦法渲染全部就直接parse了 然後就出錯 所以要check
        else:
            base_root = etree.HTML(self.driver.page_source)
            if not self.check_page_ready(base_root):
                print('request again : %s'%(url))
                self.retry_cnt+=1
                if self.retry_cnt > self.MAX_TIME_RETRY:
                    print('Retry > MAX TIME .... GG')
                    return None
                return self.send(url)
            self.retry_cnt = 0
            return self.driver.page_source
    def check_page_ready(self,base_root):
        return  len(base_root.xpath("//div[@class='result_box']//ul//li"))> 0 and len(base_root.xpath("//div[@class='result_box']//ul//li//span[@class='c_url']"))> 0
        # 有一些page只有一頁 不會出現下面的連結導航
        #return  len(base_root.xpath("//div[@class='result_box']//ul//li"))> 0 and len(base_root.xpath("//div[@class='p_pagediv']/span[@class='p_pagecur']"))>0
    




class AsyncHealthQuestionRequest():
    def __init__(self,asession,url,callback):
        self.asession = asession
        self.url = url
        self.callback = callback
    async def  send(self):
        r = await self.asession.get(self.url)
        return self.callback.on_page_loaded(r.content)

class DepartmentOfKeywordCallback():
    def __init__(self):
        pass
    def on_page_loaded(self,content):
        page = HealthQuestionPage(content)
        name,url = page.parse_nearest_department()
        return name,url



class DepartmentListRequest():
    def __init__(self,driver):
        self.driver = driver
    def send(self,url):
        try:
            self.driver.get(url)
        except:
            print('fuck %s'%(url))
            return self.send(url)
        else:
            return self.driver.page_source


class AsyncHealthPageCallback():
    def __init__(self,qid,backend=None):
        self.backend = backend
        self.qid = qid

    def on_page_loaded(self,content):
        page = HealthQuestionPage(content)
        if page.is_valid_single_question():
            title = page.parse_title()
            description = page.parse_description()
            answers = page.parse_responses()
            q = QuestionItem(self.qid,title,description)
            al = [AnswerItem(content=d['answer'],time=d['time'],job=d['job']) for d in answers]
            qa_item = qa_item = QAItem(q,al)
            if not self.backend.check_question_duplicate(self.qid):
                self.backend.save_qa_instance(qa_item)
            else:           
                print('duplicate question %s %s'%(self.qid,title))
            print('successfully parse %s'%(title))
        return None