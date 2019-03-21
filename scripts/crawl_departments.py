from src import db,crawler,util
from src.crawler import KeywordQueryRequest,AsyncHealthPageCallback,AsyncHealthQuestionRequest,\
DepartmentOfKeywordCallback,DepartmentListRequest
from src.page import KeywordQueryPage,PageUnderDepartment
from src.backend import MongoQABackend
import argparse
import config
from requests_html import AsyncHTMLSession
import re



arg_parser = argparse.ArgumentParser(description='')
arg_parser.add_argument('--url_file',default='./datas/url_for_disease_gold.txt')
args = arg_parser.parse_args()


def read_keyword_urls(path):
    with open(path,'r',encoding='utf-8') as f:
        for l in f:
            util.rlstrip(l)
            m = re.search(r'(.*)-->(.*),(.*)',l)
            kw,d,url =  m.group(1), m.group(2),m.group(3)
            yield kw,d,url
  

if __name__ == '__main__':
    print('Start scipt of crawl departments')
    connector =   db.MongoConnector(config.DB_HOST,config.DB_USER_NAME,config.DB_PASSWORD,config.DB_NAME)
    backend =  MongoQABackend(connector,config.QA_COLLECT_NAME)
    r = DepartmentListRequest(util.get_browser_driver(config.DRIVER_PATH,config.ENV))
    asession = AsyncHTMLSession()   
    for kw,dep,url in  read_keyword_urls(args.url_file):
        print('crawl %s-->%s'%(kw,url))
        current_url = url
        while current_url is not None:
            page_src = r.send(current_url)
            page =  PageUnderDepartment('呼吸內科',page_src)
            qurls = page.parse_questions()
            l = []
            for qid,link in qurls:
                cb = AsyncHealthPageCallback(qid,backend)
                arq = AsyncHealthQuestionRequest(asession,link,cb)
                l.append(arq)
            if len(l)>0:
                asession.run(*[ r.send for  r in l ])
            next_link = page.parse_next_link()
            current_url = next_link

