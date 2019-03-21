from src import db,crawler,util
from src.crawler import KeywordQueryRequest,AsyncHealthPageCallback,AsyncHealthQuestionRequest,\
DepartmentOfKeywordCallback
from src.page import KeywordQueryPage
from src.backend import MongoQABackend
import argparse
import config
from requests_html import AsyncHTMLSession
from urllib.parse import urljoin
from collections import Counter

def crawl_by_keywords(keywords):
    connector =   db.MongoConnector(config.DB_HOST,config.DB_USER_NAME,config.DB_PASSWORD,config.DB_NAME)
    backend =  MongoQABackend(connector,config.QA_COLLECT_NAME)
    keywords = util.read_txt_lines(args.kw_file)
    keywords = util.expand_keywords(keywords,['飲食'])
    kw_request = KeywordQueryRequest(util.get_browser_driver(config.DRIVER_PATH,config.ENV))
    asession = AsyncHTMLSession()
    for keyword in keywords:
        start_url ='http://so.120ask.com/?kw=%s'%(keyword)
        current_url = start_url
        while True:
            page_src = kw_request.send(current_url)
            if page_src is None:
                break
            page = KeywordQueryPage(page_src)
            links = page.parse_question_links()
            qids =  page.parse_question_ids()
            l = []
            for qid,link in zip(qids,links):
                cb = AsyncHealthPageCallback(qid,backend)
                arq = AsyncHealthQuestionRequest(asession,link,cb)
                l.append(arq)
            if len(l)>0:
                asession.run(*[ r.send for  r in l ])

            next_link = page.parse_next_page_link()
            if next_link is None:
                break
            current_url = urljoin(start_url,next_link)

def find_department_of_keywords(keywords,filepath):
    kw_request = KeywordQueryRequest(util.get_browser_driver(config.DRIVER_PATH,config.ENV))
    asession = AsyncHTMLSession()
    f = open(filepath,'w',encoding='utf-8')
    for keyword in keywords:
        start_url ='http://so.120ask.com/?kw=%s'%(keyword)
        current_url = start_url

        page_src = kw_request.send(current_url)
        assert page_src is not None
        page = KeywordQueryPage(page_src)
        links = page.parse_question_links()
        qids =  page.parse_question_ids()
        l = []
        for qid,link in zip(qids,links):
            cb = DepartmentOfKeywordCallback()
            arq = AsyncHealthQuestionRequest(asession,link,cb)
            l.append(arq)
        assert len(l) > 3
        res = asession.run(*[ r.send for  r in l ])
        # most of department of questions is the department of keyword
        c = Counter(res)
        department,url = c.most_common()[0][0]      
        f.write('%s-->%s,%s\n'%(keyword,department,url))


arg_parser = argparse.ArgumentParser(description='')
arg_parser.add_argument('--kw_file',default='./datas/disease_list.txt')
args = arg_parser.parse_args()
#arg_parser.add_argument('host')
#arg_parser.add_argument('db_name')
#arg_parser.add_argument('--password',default='')
 
if __name__=='__main__':
    find_department_of_keywords(util.read_txt_lines('./datas/disease_list_no_expand_cancer.txt'),'./datas/url_for_disease.txt')
    #crawl_by_keywords(util.read_txt_lines(args.kw_file))
    #find_department_of_keyword('糖尿病')
    #request = KeywordQueryRequest(util.get_browser_driver(config.DRIVER_PATH,config.ENV))
    #request.send('http://so.120ask.com/?kw=%s'%('878877888'))
    #request.send('http://so.120ask.com/?kw=%s'%('腸胃道間質瘤'))
    #connector =   db.MongoConnector(config.DB_HOST,config.DB_USER_NAME,config.DB_PASSWORD,config.DB_NAME)
    #backend =  backend.MongoQABackend(connector,config.QA_COLLECT_NAME)
    #crawler = crawler.Ask123Crawler(util.get_browser_driver(config.DRIVER_PATH,config.ENV),backend)
    #keywords = util.read_txt_lines(args.kw_file)
    #keywords = util.expand_keywords(keywords,['飲食'])
    #crawler.crawl_by_keywords(['腸胃道間質瘤'])
    #crawler.crawl_by_keywords(keywords)