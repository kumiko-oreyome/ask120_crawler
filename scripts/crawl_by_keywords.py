from src import db,crawler,util
from src.crawler import KeywordQueryRequest,AsyncHealthPageCallback,AsyncHealthQuestionRequest,\
DepartmentOfKeywordCallback,DepartmentListRequest
from src.page import KeywordQueryPage,PageUnderDepartment
from src.backend import MongoQABackend
import argparse
import config
from requests_html import AsyncHTMLSession
from urllib.parse import urljoin

arg_parser = argparse.ArgumentParser(description='')
arg_parser.add_argument('--kw_file',default='./datas/disease_list.txt')
args = arg_parser.parse_args()
#arg_parser.add_argument('host')
#arg_parser.add_argument('db_name')
#arg_parser.add_argument('--password',default=''


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


if __name__ == '__main__':
    keywords = util.read_txt_lines(args.kw_file)
    keywords = util.expand_keywords(keywords,['飲食'])
    crawl_by_keywords(keywords)