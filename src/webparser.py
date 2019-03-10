from lxml import etree,html
import unicodedata
import re



class QuestionListPage():
    def __init__(self,page_src):
        self.page_src = page_src
        self.base_root = etree.HTML(page_src)

    def is_valid_question_link(self,url):
        if url.startswith("http://www.120ask.com/question"):
            return True
        return False

    def check_page_ready(self):
        return  len(self.base_root.xpath("//div[@class='result_box']//ul//li"))> 0 \
                and len(self.base_root.xpath("//div[@class='p_pagediv']/span[@class='p_pagecur']"))>0
    
    def get_question_infos(self):
        assert self.check_page_ready()
        for node in self.base_root.xpath("//div[@class='result_box']//ul//span[@class='c_url']"):
            link = node.xpath("./text()")[0]
            if self.is_valid_question_link(link):
                m = re.search(r'([0-9]+)\.htm',link)
                qid = m.group(1)
                yield link,qid

    def get_next_page_link(self):
        link = self.base_root.xpath("//div[@class='p_pagediv']//a[@title='下一页']/@href")
        if len(link) == 0:
            link = None
        return link



def rlstrip(s):
   return unicodedata.normalize("NFKD", s).strip().rstrip()


def is_valid_single_question(title,description):
    return not description.startswith(title)


def parse_single_question_page(page_src):
    html_root = etree.HTML(page_src)
    title = html_root.xpath("//h1[@id='d_askH1']//text()")[0]
    #print('title %s'%(title))
    description_node = html_root.xpath("//div[@class='b_askbox']//div[@class='b_askcont']//p[@class='crazy_new']")[0]
    description = description_node.xpath("./text()")[1].strip()
    answers  = []
    #parse answers
    responses =  html_root.xpath("//div[@class='b_answerli']")
    if len(responses) == 0:
        return title,description,[{'job':'','answer':'NO_ANSWER_IN_SOURCE_PAGE','time':''}] 
    for response in responses:
        try:
            profile_box_node = response.xpath(".//div[@class='b_answertl']")[0]
            answer_box =  response.xpath(".//div[@class='b_anscontc']")[0]
            job = "".join(profile_box_node.xpath(".//span[@class='b_sp1']/text()"))
            time = answer_box.xpath(".//span[@class='b_anscont_time']/text()")[0]
            answer = answer_box.xpath(".//div[@class='crazy_new']/p")[0].xpath('string()')
            answers.append({'job':rlstrip(job),'answer':rlstrip(answer),'time':rlstrip(time)})
        except :
            print('something wrong while parsing responses of title %s'%(title))

    return title,description,answers